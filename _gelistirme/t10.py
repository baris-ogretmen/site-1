import asyncio,json,os
from harness import *
import harness
CIKTI['yonetici.html']=open('/home/claude/yama/cikti114/yonetici.html',encoding='utf8').read()
CIKTI['index.html']=open('/home/claude/yama/cikti114/index.html',encoding='utf8').read()
TREE=[l for l in os.popen("git -C /home/claude/site-1 ls-tree -r --name-only HEAD").read().split('\n') if l]
async def gapi(r):
    p=urllib.parse.urlparse(r.request.url).path[len('/repos/baris-ogretmen/site-1'):];j=lambda d:r.fulfill(body=json.dumps(d),content_type='application/json')
    if p=='':return await j({'default_branch':'main'})
    if p=='/commits':return await j([])
    if p.startswith('/git/ref/'):return await j({'object':{'sha':'c1'}})
    if p.startswith('/git/commits/'):return await j({'sha':'c1','tree':{'sha':'t1'}})
    if p.startswith('/git/trees/'):return await j({'tree':[{'path':x,'type':'blob','sha':'s','size':5000} for x in TREE]})
    return await r.fulfill(status=404,body='{}')
async def rota2(r):
    if 'api.github.com' in r.request.url:return await gapi(r)
    return await harness.rota(r)
EK="localStorage.setItem('bi_ghToken',JSON.stringify('x'));window.__DATA.projeler.p1.link='fenerr avi.html';window.__DATA.projeler.p1.kapak='gorseller/a.jpg';window.__DATA.projeler.p2.kapak='gorseller/a.jpg';"
async def main():
    async with async_playwright() as p:
        b=await tarayici(p)
        ctx=await b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True);pg=await ctx.new_page();es=[];pg.on('pageerror',lambda e:es.append(str(e)[:200]))
        await pg.add_init_script(init(True,EK));await pg.route('**/*',rota2);await pg.goto(SITE+'yonetici.html');await pg.wait_for_timeout(4500)
        await pg.add_style_tag(content='[class*=toast],[id*=toast]{display:none!important}')
        await pg.evaluate("showView('dashboard')");await pg.wait_for_timeout(800)
        print('kart:',await pg.inner_text('#sk-kart'));await pg.screenshot(path='k_p0.png')
        await pg.click('#sk-kart');await pg.wait_for_timeout(3500)
        print((await pg.inner_text('#sk-govde')).replace('\n',' | ')[:1500])
        await pg.screenshot(path='k_p1.png')
        await pg.evaluate("document.querySelector('.sk-grup:nth-of-type(3)')?.scrollIntoView()");await pg.evaluate("[...document.querySelectorAll('#sk-govde details')].forEach(d=>d.open=true)");await pg.wait_for_timeout(200)
        await pg.evaluate("document.querySelectorAll('.sk-grup')[1].scrollIntoView()");await pg.screenshot(path='k_p2.png')
        await pg.evaluate("document.querySelectorAll('.sk-grup')[2].scrollIntoView()");await pg.screenshot(path='k_p3.png')
        await pg.click('#sk-govde [data-action="edit"]');await pg.wait_for_timeout(1200);print('düzenle →',await pg.evaluate("document.getElementById('edit-title').value"))
        print('ERR',es[:3])
        ctx2=await b.new_context(viewport={'width':390,'height':844});pg2=await ctx2.new_page();await pg2.add_init_script(init(False,''));await pg2.route('**/*',rota2);await pg2.goto(SITE+'index.html');await pg2.wait_for_timeout(3500)
        print('başlık:',await pg2.title());print('dizin:',await pg2.evaluate("document.querySelector('.ft-dizin')?.innerText"),await pg2.evaluate("document.querySelectorAll('.ft-tum').length"))
        await pg2.evaluate("document.querySelector('footer').scrollIntoView()");await pg2.wait_for_timeout(400);await pg2.screenshot(path='k_site.png')
        await b.close()
asyncio.run(main())
