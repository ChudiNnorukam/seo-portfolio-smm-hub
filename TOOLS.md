# SEO Portfolio - Essential Tools

## Quick Reference Commands

Run these from the repo root (`/Users/chudinnorukam/Documents/Chudi's SEO Portfolio SMM Hub/`):

### Build & Preview
```bash
cd seo-portfolio
npm run build
npm run preview -- --port 4321
```

### Performance Testing
```bash
# Single page Lighthouse audit
npx lighthouse http://localhost:4321 --output=json --output-path=./lighthouse-report.json

# Full LHCI audit (multiple pages)
npx @lhci/cli@0.13.x autorun --collect.url=http://localhost:4321 --upload.target=filesystem --upload.outputDir=./lhci-reports

# Performance check script
./scripts/check-performance.sh
```

### Accessibility Testing
```bash
# Quick accessibility check
npx pa11y http://localhost:4321

# Lighthouse accessibility (included in full audit)
npx lighthouse http://localhost:4321 --only-categories=accessibility
```

### JSON Processing
```bash
# Parse Lighthouse results
jq '.categories.performance.score * 100' lighthouse-report.json
jq '.audits["largest-contentful-paint"].numericValue' lighthouse-report.json

# Check budget compliance
node -e "const budget = require('./perf-budget.json'); const report = JSON.parse(require('fs').readFileSync('./lighthouse-report.json')); console.log('LCP:', report.audits['largest-contentful-paint'].numericValue, 'ms (budget:', budget.lcp, 'ms)');"
```

### Content Verification
```bash
# Check sitemap
curl -s "http://localhost:4321/sitemap" | grep -o 'href="/blog/[^"]*"' | wc -l

# Verify interlinking
curl -s "http://localhost:4321/blog/ai-mvp-builder-vs-no-code" | grep -A 10 "Further Reading"

# Check schema markup
curl -s "http://localhost:4321/blog/ai-mvp-builder-vs-no-code" | grep -A 50 'application/ld+json'
```

## Tool Installation

### Required (Node 20+)
```bash
# Already installed via package.json
npm install
```

### Optional Helpers
```bash
# Global Lighthouse CI
npm i -g @lhci/cli

# Accessibility testing
npm i -g pa11y

# JSON processing (macOS)
brew install jq

# JSON processing (Ubuntu/Debian)
sudo apt install jq
```

## Development Workflow

### 1. Local Development
```bash
cd seo-portfolio
npm run dev
# Visit http://localhost:4321
```

### 2. Build & Test
```bash
cd seo-portfolio
npm run build
npx serve dist -p 4321 &
./scripts/check-performance.sh
```

### 3. CI/CD Testing
```bash
# Test the full CI pipeline locally
cd seo-portfolio
npm run build
npx serve dist -p 4321 &
npx @lhci/cli@0.13.x autorun --collect.url=http://localhost:4321 --upload.target=filesystem --upload.outputDir=./lhci-reports
```

## Performance Budgets

Current thresholds in `perf-budget.json`:
- **LCP**: ≤2,500ms
- **CLS**: ≤0.1
- **INP**: ≤200ms
- **FCP**: ≤1,800ms
- **SI**: ≤3,000ms
- **TTI**: ≤3,800ms

## Key URLs for Testing

- **Homepage**: http://localhost:4321/
- **Blog Index**: http://localhost:4321/blog
- **Cornerstone Article**: http://localhost:4321/blog/ai-mvp-builder-vs-no-code
- **Social Hub**: http://localhost:4321/social-hub
- **Sitemap**: http://localhost:4321/sitemap

## Browser Testing

Point a modern browser to `http://localhost:4321` for:
- Visual regression testing
- Manual accessibility checks
- User experience validation
- Cross-browser compatibility

## Troubleshooting

### Build Issues
```bash
# Clear cache and rebuild
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Performance Issues
```bash
# Check bundle size
npm run build
du -sh dist/

# Analyze Lighthouse report
npx lighthouse http://localhost:4321 --view
```

### Content Issues
```bash
# Verify all blog posts are built
ls -la seo-portfolio/dist/blog/

# Check for missing content
find seo-portfolio/src/content/blog -name "*.md" | wc -l
```
