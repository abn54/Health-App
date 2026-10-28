// Development-only manual review harness. Run the app with ?a11y-review in Vite.
// All app interactions stay manual; this button runs read-only axe checks.
const panel = document.createElement('aside')
panel.id = 'audit-review-tools'
panel.setAttribute('aria-label','Development accessibility review')
panel.style.cssText = 'position:fixed;top:0;left:0;max-width:260px;z-index:100;background:white;color:#111;border:2px solid #245a91;padding:8px;max-height:65px;overflow:auto;font:14px system-ui'
const run = document.createElement('button')
run.textContent = 'Run accessibility audit'
run.style.cssText = 'background:#245a91;color:white;padding:10px;border-radius:5px'
const output = document.createElement('pre')
output.id = 'audit-output'
output.textContent = 'Audit not run. Manual keyboard and screen-reader review is still required.'
output.style.cssText = 'white-space:pre-wrap;font:12px monospace'
panel.append(run,output)
document.body.append(panel)
run.onclick = async () => {
  run.disabled = true; output.textContent = 'Audit running…'
  try {
    const {default:axe} = await import('axe-core')
    const results = await axe.run({exclude:[['#audit-review-tools']]},{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa','best-practice']}})
    output.textContent = JSON.stringify({version:axe.version,date:new Date().toISOString(),violations:results.violations.map(r=>({id:r.id,impact:r.impact,help:r.help,nodes:r.nodes.map(n=>({target:n.target,html:n.html,summary:n.failureSummary}))})),incomplete:results.incomplete.map(r=>({id:r.id,targets:r.nodes.map(n=>n.target)})),passedRules:results.passes.length},null,2)
  } catch(error) { output.textContent = 'Audit failed: '+error.message }
  finally { run.disabled = false }
}
