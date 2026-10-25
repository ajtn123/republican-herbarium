import asyncio,json
from playwright.async_api import async_playwright
BASE='http://127.0.0.1:4321'
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
  page=await browser.new_page(viewport={'width':1440,'height':1080},device_scale_factor=1)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  response=await page.goto(BASE);assert response.status==200
  await page.wait_for_function("document.querySelector('#decimal-time').textContent.includes(':') && !document.querySelector('#decimal-time').textContent.includes('—')")
  await page.screenshot(path='/workspace/shared/republican-qa/home-desktop.png',full_page=True)
  await page.click('.search-trigger');await page.fill('#global-search','raisin');await page.wait_for_selector('#search-results a');assert await page.locator('#search-results a').count()==1
  await page.click('#search-results a');await page.wait_for_url('**/days/vendemiaire-01/');assert await page.locator('h1').inner_text()=='葡萄'
  await page.screenshot(path='/workspace/shared/republican-qa/day-desktop.png',full_page=True)
  await page.goto(BASE+'/atlas/');await page.select_option('#atlas-category','大地材料');assert await page.locator('.day-cell:visible').count()==24
  await page.fill('#atlas-query','煤');assert await page.locator('.day-cell:visible').count()==1
  await page.fill('#atlas-query','不存在');assert await page.locator('#atlas-empty').is_visible()
  await page.click('button[type=reset]');await page.wait_for_function("document.querySelectorAll('.day-cell:not([hidden])').length===360")
  await page.goto(BASE+'/time/');await page.fill('#gregorian-date','1794-07-27');await page.click('#panel-gregorian button');assert '热月 9 日' in await page.locator('#converted-date').inner_text()
  await page.fill('#gregorian-date','1795-09-22');await page.click('#panel-gregorian button');assert '革命节' in await page.locator('#converted-date').inner_text()
  await page.click('#tab-republican');await page.fill('#republican-year','3');await page.select_option('#republican-month','13');await page.fill('#republican-day','6');await page.click('#panel-republican button');assert '1795 年 9 月 22 日' in await page.locator('#converted-date').inner_text()
  await page.fill('#republican-year','4');assert await page.locator('#republican-day').get_attribute('max')=='5'
  await page.goto(BASE+'/months/brumaire/');await page.screenshot(path='/workspace/shared/republican-qa/month-desktop.png',full_page=True)
  await page.set_viewport_size({'width':390,'height':844})
  for route,label in [('/','home'),('/days/nivose-23/','mineral'),('/months/floreal/','month'),('/time/','time'),('/festivals/opinion/','festival'),('/history/','history'),('/atlas/','atlas')]:
   await page.goto(BASE+route);await page.evaluate('document.fonts.ready');assert await page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'),f'overflow {route}'
   if label in ['home','mineral','time']:await page.screenshot(path=f'/workspace/shared/republican-qa/{label}-mobile.png',full_page=True)
  await browser.close();assert not errors,errors
  print(json.dumps({'browser_errors':errors,'desktop_mobile':'passed','search':'passed','filters':'passed','historical_and_leap_dates':'passed'},ensure_ascii=False))
asyncio.run(main())
