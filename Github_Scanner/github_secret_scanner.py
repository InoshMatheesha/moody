"""
GitHub Secret Scanner
A secure Python script that scans your GitHub repositories for leaked secrets.
Only scans repositories under your own GitHub account.
"""

import requests
import re
import json
import time
import base64
from datetime import datetime
from typing import Optional

# ANSI color codes for console output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


# Keywords and patterns to search for
SECRET_PATTERNS = {
    'high': [
        (r'discord\.com/api/webhooks/\d+/[\w-]+', 'Discord Webhook URL'),
        (r'ghp_[a-zA-Z0-9]{36}', 'GitHub Personal Access Token'),
        (r'gho_[a-zA-Z0-9]{36}', 'GitHub OAuth Token'),
        (r'ghu_[a-zA-Z0-9]{36}', 'GitHub User Token'),
        (r'ghs_[a-zA-Z0-9]{36}', 'GitHub Server Token'),
        (r'ghr_[a-zA-Z0-9]{36}', 'GitHub Refresh Token'),
        (r'AKIA[0-9A-Z]{16}', 'AWS Access Key ID'),
        (r'sk-[a-zA-Z0-9]{48}', 'OpenAI API Key'),
        (r'xox[baprs]-[0-9a-zA-Z-]+', 'Slack Token'),
        (r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----', 'Private Key'),
        (r'AIza[0-9A-Za-z\\-_]{35}', 'Google API Key'),
    ],
    'medium': [
        (r'api[_-]?key["\']?\s*[:=]\s*["\'][a-zA-Z0-9]{16,}["\']', 'API Key Assignment'),
        (r'api[_-]?secret["\']?\s*[:=]\s*["\'][a-zA-Z0-9]{16,}["\']', 'API Secret Assignment'),
        (r'token["\']?\s*[:=]\s*["\'][a-zA-Z0-9]{16,}["\']', 'Token Assignment'),
        (r'password["\']?\s*[:=]\s*["\'][^"\']{8,}["\']', 'Password Assignment'),
        (r'secret["\']?\s*[:=]\s*["\'][a-zA-Z0-9]{16,}["\']', 'Secret Assignment'),
        (r'webhook["\']?\s*[:=]\s*["\']https?://[^"\']+["\']', 'Webhook URL'),
    ],
    'low': [
        (r'private[_-]?key', 'Private Key Reference'),
        (r'api[_-]?key', 'API Key Reference'),
        (r'access[_-]?token', 'Access Token Reference'),
        (r'auth[_-]?token', 'Auth Token Reference'),
        (r'client[_-]?secret', 'Client Secret Reference'),
    ]
}

# Search keywords for GitHub Code Search API
SEARCH_KEYWORDS = [
    "discord.com/api/webhooks",
    "webhook",
    "api_key",
    "token",
    "password",
    "private_key",
    "secret",
    "credentials"
]


class GitHubSecretScanner:
    def __init__(self, username: str, token: str):
        self.username = username
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.results = []
        self.rate_limit_remaining = 5000
        self.rate_limit_reset = 0
        
    def print_colored(self, message: str, color: str = Colors.WHITE):
        """Print colored message to console."""
        print(f"{color}{message}{Colors.RESET}")
    
    def print_banner(self):
        """Print the scanner banner."""
        banner = """
╔═══════════════════════════════════════════════════════════════╗
║           GitHub Secret Scanner - Security Tool               ║
║     Scans YOUR repositories for potential leaked secrets      ║
╚═══════════════════════════════════════════════════════════════╝
        """
        self.print_colored(banner, Colors.CYAN)
    
    def check_rate_limit(self):
        """Check GitHub API rate limit and wait if necessary."""
        if self.rate_limit_remaining < 10:
            wait_time = max(0, self.rate_limit_reset - time.time()) + 1
            if wait_time > 0:
                self.print_colored(f"⏳ Rate limit low. Waiting {wait_time:.0f} seconds...", Colors.YELLOW)
                time.sleep(wait_time)
    
    def update_rate_limit(self, response: requests.Response):
        """Update rate limit info from response headers."""
        self.rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 5000))
        self.rate_limit_reset = int(response.headers.get('X-RateLimit-Reset', 0))
    
    def make_request(self, url: str, params: Optional[dict] = None) -> Optional[requests.Response]:
        """Make a rate-limited request to GitHub API."""
        self.check_rate_limit()
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            self.update_rate_limit(response)
            
            if response.status_code == 403 and 'rate limit' in response.text.lower():
                self.print_colored("⚠️ Rate limit exceeded. Waiting for reset...", Colors.YELLOW)
                time.sleep(60)
                return self.make_request(url, params)
            
            return response
        except requests.exceptions.RequestException as e:
            self.print_colored(f"❌ Request error: {e}", Colors.RED)
            return None
    
    def verify_credentials(self) -> bool:
        """Verify GitHub credentials and username match."""
        self.print_colored("\n🔐 Verifying credentials...", Colors.BLUE)
        
        response = self.make_request(f"{self.base_url}/user")
        
        if response is None or response.status_code != 200:
            self.print_colored("❌ Invalid GitHub credentials!", Colors.RED)
            return False
        
        user_data = response.json()
        authenticated_user = user_data.get('login', '')
        
        if authenticated_user.lower() != self.username.lower():
            self.print_colored(f"❌ Token belongs to '{authenticated_user}', not '{self.username}'!", Colors.RED)
            self.print_colored("⚠️ For security, you can only scan your own repositories.", Colors.YELLOW)
            return False
        
        self.print_colored(f"✅ Authenticated as: {authenticated_user}", Colors.GREEN)
        return True
    
    def get_user_repos(self) -> list:
        """Get all repositories for the authenticated user."""
        self.print_colored("\n📂 Fetching your repositories...", Colors.BLUE)
        
        repos = []
        page = 1
        
        while True:
            response = self.make_request(
                f"{self.base_url}/user/repos",
                params={'per_page': 100, 'page': page, 'affiliation': 'owner'}
            )
            
            if response is None or response.status_code != 200:
                break
            
            page_repos = response.json()
            if not page_repos:
                break
            
            repos.extend(page_repos)
            page += 1
            
            # Small delay to be respectful to API
            time.sleep(0.5)
        
        self.print_colored(f"📊 Found {len(repos)} repositories", Colors.GREEN)
        return repos
    
    def get_repo_contents(self, repo_name: str, path: str = "") -> list:
        """Recursively get all files in a repository."""
        files = []
        
        response = self.make_request(
            f"{self.base_url}/repos/{self.username}/{repo_name}/contents/{path}"
        )
        
        if response is None or response.status_code != 200:
            return files
        
        contents = response.json()
        
        if isinstance(contents, dict):
            contents = [contents]
        
        for item in contents:
            if item['type'] == 'file':
                # Skip binary files and large files
                if item.get('size', 0) < 500000:  # Skip files > 500KB
                    files.append({
                        'path': item['path'],
                        'sha': item['sha'],
                        'download_url': item.get('download_url'),
                        'size': item.get('size', 0)
                    })
            elif item['type'] == 'dir':
                # Skip common non-relevant directories
                skip_dirs = ['node_modules', '.git', 'vendor', 'dist', 'build', '__pycache__', '.next']
                if item['name'] not in skip_dirs:
                    files.extend(self.get_repo_contents(repo_name, item['path']))
                    time.sleep(0.2)  # Rate limiting
        
        return files
    
    def get_file_content(self, download_url: str) -> Optional[str]:
        """Download and return file content."""
        if not download_url:
            return None
        
        try:
            response = requests.get(download_url, timeout=30)
            if response.status_code == 200:
                return response.text
        except:
            pass
        
        return None
    
    def scan_content(self, content: str, file_path: str, repo_name: str):
        """Scan file content for secrets."""
        findings = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Skip empty lines and comments
            stripped = line.strip()
            if not stripped or stripped.startswith('#') or stripped.startswith('//'):
                continue
            
            for risk_level, patterns in SECRET_PATTERNS.items():
                for pattern, description in patterns:
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        # Skip if it looks like a placeholder or example
                        matched_text = match.group()
                        if self.is_placeholder(matched_text, line):
                            continue
                        
                        finding = {
                            'repo': repo_name,
                            'file_path': file_path,
                            'line_number': line_num,
                            'line_snippet': self.truncate_line(line),
                            'risk_level': risk_level,
                            'secret_type': description,
                            'matched_pattern': matched_text[:50] + '...' if len(matched_text) > 50 else matched_text
                        }
                        findings.append(finding)
        
        return findings
    
    def is_placeholder(self, matched_text: str, line: str) -> bool:
        """Check if the match is likely a placeholder or example."""
        placeholders = [
            'your_', 'my_', 'example', 'placeholder', 'xxx', 'yyy', 'zzz',
            'insert', 'enter', 'replace', 'todo', 'fixme', '<', '>', '{', '}',
            'sample', 'test', 'demo', 'fake', 'dummy'
        ]
        
        lower_text = matched_text.lower()
        lower_line = line.lower()
        
        for placeholder in placeholders:
            if placeholder in lower_text or placeholder in lower_line:
                return True
        
        # Check if it's in a comment
        if '# ' in line or '//' in line or '/*' in line:
            return True
        
        return False
    
    def truncate_line(self, line: str, max_length: int = 100) -> str:
        """Truncate line for display, masking potential secrets."""
        line = line.strip()
        if len(line) > max_length:
            line = line[:max_length] + '...'
        return line
    
    def search_commits(self, repo_name: str) -> list:
        """Search through commit messages and diffs for secrets."""
        findings = []
        
        response = self.make_request(
            f"{self.base_url}/repos/{self.username}/{repo_name}/commits",
            params={'per_page': 50}
        )
        
        if response is None or response.status_code != 200:
            return findings
        
        commits = response.json()
        
        for commit in commits[:20]:  # Limit to recent 20 commits
            sha = commit['sha']
            
            # Get commit details
            commit_response = self.make_request(
                f"{self.base_url}/repos/{self.username}/{repo_name}/commits/{sha}"
            )
            
            if commit_response is None or commit_response.status_code != 200:
                continue
            
            commit_data = commit_response.json()
            
            # Check commit message
            message = commit_data.get('commit', {}).get('message', '')
            message_findings = self.scan_content(message, f"commit:{sha[:7]}", repo_name)
            findings.extend(message_findings)
            
            # Check file patches
            files = commit_data.get('files', [])
            for file in files:
                patch = file.get('patch', '')
                if patch:
                    file_findings = self.scan_content(patch, f"{file['filename']} (commit:{sha[:7]})", repo_name)
                    findings.extend(file_findings)
            
            time.sleep(0.3)  # Rate limiting
        
        return findings
    
    def scan_repo(self, repo: dict):
        """Scan a single repository for secrets."""
        repo_name = repo['name']
        self.print_colored(f"\n🔍 Scanning: {repo_name}", Colors.BLUE)
        
        # Get all files
        files = self.get_repo_contents(repo_name)
        self.print_colored(f"   📄 Found {len(files)} files to scan", Colors.WHITE)
        
        # Scan each file
        for file_info in files:
            content = self.get_file_content(file_info['download_url'])
            if content:
                findings = self.scan_content(content, file_info['path'], repo_name)
                self.results.extend(findings)
                
                # Report findings immediately
                for finding in findings:
                    self.report_finding(finding)
            
            time.sleep(0.1)  # Rate limiting
        
        # Search commits
        self.print_colored(f"   📝 Scanning recent commits...", Colors.WHITE)
        commit_findings = self.search_commits(repo_name)
        self.results.extend(commit_findings)
        
        for finding in commit_findings:
            self.report_finding(finding)
    
    def report_finding(self, finding: dict):
        """Report a single finding with colored output."""
        risk_level = finding['risk_level']
        
        if risk_level == 'high':
            color = Colors.RED
            icon = '🚨'
        elif risk_level == 'medium':
            color = Colors.YELLOW
            icon = '⚠️'
        else:
            color = Colors.CYAN
            icon = 'ℹ️'
        
        self.print_colored(f"\n{icon} {risk_level.upper()} RISK FINDING", color + Colors.BOLD)
        self.print_colored(f"   Repository: {finding['repo']}", color)
        self.print_colored(f"   File: {finding['file_path']}", color)
        self.print_colored(f"   Line: {finding['line_number']}", color)
        self.print_colored(f"   Type: {finding['secret_type']}", color)
        self.print_colored(f"   Snippet: {finding['line_snippet']}", Colors.WHITE)
    
    def print_summary(self):
        """Print summary of scan results."""
        self.print_colored("\n" + "=" * 60, Colors.CYAN)
        self.print_colored("                    SCAN SUMMARY", Colors.CYAN + Colors.BOLD)
        self.print_colored("=" * 60, Colors.CYAN)
        
        high_count = sum(1 for r in self.results if r['risk_level'] == 'high')
        medium_count = sum(1 for r in self.results if r['risk_level'] == 'medium')
        low_count = sum(1 for r in self.results if r['risk_level'] == 'low')
        total = len(self.results)
        
        self.print_colored(f"\n📊 Total Potential Leaks Found: {total}", Colors.WHITE + Colors.BOLD)
        self.print_colored(f"   🚨 High Risk:   {high_count}", Colors.RED)
        self.print_colored(f"   ⚠️  Medium Risk: {medium_count}", Colors.YELLOW)
        self.print_colored(f"   ℹ️  Low Risk:    {low_count}", Colors.CYAN)
        
        if total > 0:
            self.print_colored("\n⚠️ RECOMMENDATION: Review all findings and rotate any exposed secrets!", Colors.YELLOW)
        else:
            self.print_colored("\n✅ No potential secrets detected!", Colors.GREEN)
        
        self.print_colored("=" * 60 + "\n", Colors.CYAN)
    
    def save_results(self, filename: str = "scan_results.json"):
        """Save results to JSON file."""
        output = {
            'scan_date': datetime.now().isoformat(),
            'scanned_user': self.username,
            'total_findings': len(self.results),
            'summary': {
                'high_risk': sum(1 for r in self.results if r['risk_level'] == 'high'),
                'medium_risk': sum(1 for r in self.results if r['risk_level'] == 'medium'),
                'low_risk': sum(1 for r in self.results if r['risk_level'] == 'low')
            },
            'findings': self.results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        self.print_colored(f"💾 Results saved to: {filename}", Colors.GREEN)
    
    def run(self):
        """Main scanning workflow."""
        self.print_banner()
        
        # Verify credentials
        if not self.verify_credentials():
            return
        
        # Get user repos
        repos = self.get_user_repos()
        
        if not repos:
            self.print_colored("❌ No repositories found!", Colors.RED)
            return
        
        # Scan each repo
        self.print_colored(f"\n🚀 Starting scan of {len(repos)} repositories...", Colors.GREEN)
        
        for i, repo in enumerate(repos, 1):
            self.print_colored(f"\n[{i}/{len(repos)}] ", Colors.MAGENTA, )
            self.scan_repo(repo)
        
        # Print summary
        self.print_summary()
        
        # Save results
        save_option = input("💾 Save results to JSON file? (y/n): ").strip().lower()
        if save_option == 'y':
            self.save_results()


def main():
    """Main entry point."""
    print("\n" + "=" * 60)
    print("       GitHub Secret Scanner - Secure Credential Check")
    print("=" * 60)
    print("\n⚠️  This tool only scans YOUR OWN repositories.")
    print("⚠️  Never use this to scan other people's repositories.")
    print("⚠️  This tool only detects and reports - no exploitation.\n")
    
    # Get credentials
    username = input("👤 Enter your GitHub username: ").strip()
    if not username:
        print("❌ Username is required!")
        return
    
    print("\n📝 Note: Create a Personal Access Token at:")
    print("   https://github.com/settings/tokens")
    print("   Required scopes: repo (for private repos) or public_repo (public only)\n")
    
    token = input("🔑 Enter your GitHub Personal Access Token: ").strip()
    if not token:
        print("❌ Token is required!")
        return
    
    # Create scanner and run
    scanner = GitHubSecretScanner(username, token)
    scanner.run()


if __name__ == "__main__":
    main()
