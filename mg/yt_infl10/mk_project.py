# YT 10 – "Why Is Everything So Expensive?" -> project.json
# Sources (all checked 2026-10-23): BLS CPI release Sep 2026 (USDL-26-1574); FRED/BLS average prices
# APU0000717311 coffee 4.174->9.332, APU0000703112 beef 3.886->6.792, APU000074714 gas 2.567->4.482,
# APU000072610 electricity 0.134->0.196 (Jan 2020 -> Sep 2026); CPI-U 257.971 (Jan 2020) -> 336.940 (Sep 2026) = +30.6%;
# CES0500000003 avg hourly earnings 28.43 -> 37.81 (+33.0%); BLS TED real AHE -0.7% Sep25-Sep26;
# FRED M2SL 15,492.8 (Feb 2020) -> 21,788.1 (Mar 2022) = +40.6%; EIA: Brent $61 -> $118 Q1 2026, Hormuz;
# Bernanke & Blanchard (NBER/Brookings 2023); KC Fed (profits 41% vs 59% earlier recoveries), SF Fed (markups flat);
# BLS Beyond the Numbers vol. 12 (shrinkflation, 220->200 sheets example). June 2022 CPI 9.1% = highest since Nov 1981.
import json,os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def I(lay,img,ov,**k): return dict(type="img",lay=lay,img=img,ov=ov,**k)
def PH(n,title,img): return dict(type="phase",n=n,title=title,img=img)
def ch(*items,title=None,flow=False): return dict(title=title,items=[list(i) for i in items],flow=flow)
L=[]
def A(t,s): L.append((t,s))
# ---------------------------------------------------------------- HOOK
A("In 2020, a pound of coffee cost about four dollars. Today, it costs over nine.",dict(type="hook",img=103))
A("Ground beef went from under four dollars to almost seven. And a gallon of gas, from about two fifty to almost four fifty.",I("right",102,"rows",title="Then vs. now",rows=[["Ground beef, 1 lb","$3.89 → $6.79","red","beef"],["Gasoline, 1 gallon","$2.57 → $4.48","red","gas"]]))
A("So why is everything so expensive? Why do prices never go back down? And at the end, there is one number that might surprise you.",I("left",101,"chips",**ch(["Why so expensive?","lens","expensive"],["Why no way back?","down","never"],["One surprising number","bulb","surprise"],title="Today")))
A("Quick note: all numbers are United States data from the Bureau of Labor Statistics and the Federal Reserve. This is not financial advice.",I("full",104,"stamp",text="U.S. data · BLS & Fed",sub="education only, not financial advice",col="gold",x=1400,y=130))
# ---------------------------------------------------------------- 1
A("Phase one: the receipt.",PH(1,"The receipt",101))
A("Let us start with the receipt. Since January 2020, coffee is up about one hundred twenty-four percent.",dict(type="receipt",group="rcpt",img=101))
A("Ground beef, up seventy-five percent. Gasoline, also up about seventy-five percent.",dict(type="receipt",group="rcpt",img=101))
A("And electricity, up forty-six percent.",dict(type="receipt",group="rcpt",img=101))
A("Across everything people buy, prices are up about thirty-one percent on average.",dict(type="stat",value=30.6,dec=1,pre="+",suf=" %",label="average price level",sub="Consumer Price Index, Jan 2020 → Sep 2026 (BLS)",img=104))
A("In other words: what cost one hundred dollars in 2020 now costs about one hundred thirty-one.",dict(type="money",img=101,to=131,re="thirty",top="Same stuff, Jan 2020 → Sep 2026",lab="for what cost $100",sub="based on the CPI"))
# ---------------------------------------------------------------- 2
A("Phase two: what inflation really is.",PH(2,"What inflation really is",104))
A("That average is called inflation. Every month, the government tracks the prices of thousands of things: food, rent, gas, phone plans, and much more.",I("left",104,"chips",**ch(["Food","bread","food"],["Rent","house","rent"],["Gas","oil","gas"],["Phone plans","phone","phone"],title="The CPI basket")))
A("A healthy economy usually has around two percent per year. In June 2022, it hit nine point one percent, the highest in about forty years.",I("right",101,"vs",title="Inflation per year",a=["Typical target","≈ 2 %","green","two"],b=["June 2022","9.1 %","red","nine"],foot="highest since 1981 (BLS)"))
A("Two percent sounds tiny. But at two percent a year, prices double in about thirty-five years. At nine percent, they double in only about eight.",I("left",104,"rows",title="Rule of 70",rows=[["At 2 % per year","prices × 2 in ≈ 35 years","green","two"],["At 9 % per year","prices × 2 in ≈ 8 years","red","nine"]]))
A("So what pushed prices up so fast? There are three big causes.",I("full",107,"stamp",text="3 big causes",sub="",col="gold",x=1450,y=130))
# ---------------------------------------------------------------- 3
A("Phase three: too much money, too few goods.",PH(3,"More money, fewer goods",105))
A("In 2020, the pandemic broke global supply chains. Factories closed, ships waited for weeks outside ports, and shelves went empty.",I("left",106,"chips",**ch(["Factories closed","gear","factories"],["Ships waiting","truck","ships"],["Empty shelves","cart","shelves"],title="Supply shock")))
A("Used cars are a famous example. A chip shortage slowed down car factories, and by June 2021, used car prices were up forty-five percent in just one year.",dict(type="stat",value=45.2,dec=1,pre="+",suf=" %",label="used cars, June 2021 vs. a year earlier",sub="CPI, used cars and trucks (BLS)",img=107))
A("At the same time, the government sent out stimulus checks, and the Federal Reserve pushed trillions of dollars into the economy.",dict(type="m2",group="m2",img=105))
A("The money supply, called M2, jumped from about fifteen and a half trillion dollars to almost twenty-two trillion in two years. That is about forty percent more money.",dict(type="m2",group="m2",img=105))
A("More money chasing fewer goods. That is the classic recipe for inflation.",I("right",107,"vs",title="The recipe",a=["Money","more","gold","money"],b=["Goods","fewer","red","goods"]))
# ---------------------------------------------------------------- 4
A("Phase four: energy shocks.",PH(4,"Energy shocks",108))
A("Energy is in almost everything. Every product has to be made, heated, and shipped.",I("left",108,"chips",**ch(["Made","gear","made"],["Heated","bolt","heated"],["Shipped","truck","shipped"],title="Energy is everywhere",flow=True)))
A("In 2022, the war in Ukraine sent energy prices soaring. And in 2026, it happened again.",I("full",108,"stamp",text="2022 … and 2026",sub="two energy shocks",col="red",x=1400,y=130))
A("After military conflict broke out in the Middle East at the end of February 2026, shipping through the Strait of Hormuz nearly stopped.",dict(type="oil",group="oil",img=108))
A("The price of Brent crude oil jumped from sixty-one dollars to one hundred eighteen dollars a barrel in about three months.",dict(type="oil",group="oil",img=108))
A("By September 2026, gasoline cost thirty-four percent more than a year earlier.",dict(type="stat",value=34.2,dec=1,pre="+",suf=" %",label="gasoline vs. one year earlier",sub="CPI, September 2026 (BLS)",img=102))
# ---------------------------------------------------------------- 5
A("Phase five: wages.",PH(5,"Wages",109))
A("When everything gets more expensive, workers ask for higher pay. And when there are more jobs than workers, they get it.",I("left",109,"chips",**ch(["Prices up","up","expensive","red"],["Workers want more","heart","pay"],["Many open jobs","flag","jobs"],title="The job market")))
A("But higher wages mean higher costs for companies, so prices go up again.",I("right",109,"chips",**ch(["Prices ↑","up","higher"],["Wages ↑","coin","wages"],["Prices ↑ again","up","again","red"],title="The spiral",flow=True)))
A("Economists Ben Bernanke and Olivier Blanchard found that energy, food, and shortages started the inflation, and a tight job market kept it going.",I("left",104,"rows",title="Bernanke & Blanchard (2023)",rows=[["What started it","energy, food, shortages","gold","started"],["What kept it going","tight job market","red","going"]]))
# ---------------------------------------------------------------- 6
A("Phase six: what about greedy companies?",PH(6,"Greedy companies?",110))
A("Many people blame corporate greed. And companies did raise prices, and profits went up.",I("left",110,"chips",**ch(["Prices raised","up","raise"],["Profits up","coin","profits"],title="The accusation")))
A("A study by the Kansas City Fed found that profits explained about forty-one percent of price growth in the first two years of the recovery. But in earlier recoveries, that share was even higher: about fifty-nine percent.",I("right",110,"vs",title="Kansas City Fed",a=["Profit share, 2020–21","41 %","red","forty"],b=["Earlier recoveries","59 %","gold","fifty"]))
A("And the San Francisco Fed found that profit margins across the whole economy stayed roughly flat. So greed alone does not explain it, but it is still part of the debate.",I("left",110,"chips",**ch(["SF Fed: margins ≈ flat","lens","flat"],["Not the main driver","cross","alone"],["Still debated","heart","debate"],title="The other side")))
A("Then there is shrinkflation: same price, smaller package.",dict(type="shrink",group="shrink",img=111))
A("For example, if a toilet paper roll goes from two hundred twenty sheets to two hundred, you pay about ten percent more per sheet.",dict(type="shrink",group="shrink",img=111))
A("The Bureau of Labor Statistics does count this in inflation. Overall, the effect is small, but for paper products and snacks it adds up.",I("full",111,"stamp",text="Counted in the CPI",sub="small overall, bigger for snacks & paper",col="gold",x=1400,y=130))
# ---------------------------------------------------------------- 7
A("Phase seven: why prices do not come back down.",PH(7,"Why prices stay high",112))
A("Here is the frustrating part. When inflation falls, prices do not go down. They just rise more slowly.",I("right",112,"vs",title="The misunderstanding",a=["Inflation falls","prices rise slower","gold","falls"],b=["Prices fall","almost never","red","down"]))
A("For prices to actually fall, you need deflation. That usually happens in deep crises, like the Great Depression, when businesses fail and people lose their jobs.",I("left",112,"chips",**ch(["Deflation","down","deflation"],["Deep crises","warn","crises","red"],["Lost jobs","cross","jobs","red"],title="Falling prices")))
A("So central banks aim for small, steady inflation instead. Which means today's prices are probably here to stay.",I("full",101,"stamp",text="Here to stay",sub="",col="red",x=1450,y=130))
A("And pay almost never gets cut. So once prices and wages have moved up together, the whole economy settles at the new, higher level.",I("left",113,"chips",**ch(["Wages rarely fall","shield","cut"],["New, higher level","up","level"],title="Why it sticks")))
# ---------------------------------------------------------------- 8
A("Phase eight: the surprising number.",PH(8,"The surprising number",113))
A("Now the number I promised. Since January 2020, prices are up about thirty-one percent.",dict(type="wages",group="wages",img=113))
A("But the average hourly wage went from twenty-eight dollars and forty-three cents to thirty-seven eighty-one. That is up about thirty-three percent.",dict(type="wages",group="wages",img=113))
A("So on average, wages actually grew a little faster than prices.",dict(type="wages",group="wages",img=113))
A("But there are two big catches. First: in the last twelve months, prices rose faster than pay again. Real wages fell by zero point seven percent.",I("right",102,"vs",title="Catch number 1",a=["Real wages, Sep 2025 → Sep 2026","−0.7 %","red","real"],b=["Reason","energy shock","gold","prices"]))
A("And second: that is an average. If your pay did not rise by at least thirty-one percent since 2020, you are poorer than you were.",I("left",103,"stamp",text="Catch number 2",sub="pay up less than 31 %? You lost ground.",col="red"))
# ---------------------------------------------------------------- 9
A("Phase nine: what you can do.",PH(9,"What you can do",114))
A("First: know your number. If your pay has not kept up with inflation, that is a strong argument for a raise, or for a new job.",I("left",109,"chips",**ch(["Know your number","lens","number"],["Ask for a raise","up","raise"],["Or switch jobs","flag","job"],title="1 · Your pay")))
A("Second: compare the price per unit, not the price on the package. That is how you catch shrinkflation.",I("right",114,"chips",**ch(["Price per ounce","pct","unit"],["Not per package","cross","package"],title="2 · Unit prices")))
A("Third: do not let too much money sit in cash. One hundred dollars from 2020 now buys only about seventy-seven dollars worth of stuff.",dict(type="money",img=112,to=77,re="seventy",top="$100 kept as cash since 2020",lab="real buying power today",sub="based on the CPI"))
A("Many people put long-term savings into investments that have historically grown faster than inflation, like broad index funds. But nothing is guaranteed, so do your own research.",I("left",115,"chips",**ch(["Long-term investing","up","investments"],["Broad index funds","globe","index"],["No guarantees","warn","guaranteed"],title="3 · Your savings")))
# ---------------------------------------------------------------- END
A("So, why is everything so expensive? Too much money, too few goods, energy shocks, and a hot job market. And once prices go up, they rarely come back down.",I("right",101,"chips",**ch(["More money, fewer goods","coin","money"],["Energy shocks","oil","energy"],["Hot job market","up","job"],["Prices stay high","flag","rarely"],title="The answer")))
A("Now tell me in the comments: which price shocked you the most?",I("left",102,"chips",**ch(["Which price?","bell","price"],["Comment below","heart","comments"],title="Your turn")))
A("And subscribe for more money explained simply. Next: why rich people pay less tax than you.",dict(type="outro",img=116))
cfg={"title":"YouTube: Why Is Everything So Expensive?","size":[1920,1080],"fps":30,"scene":"scene.html",
 "voice":"en-US-AndrewMultilingualNeural","rate":"+10%","lead":0.6,"gap":0.4,"tail":3.0,"crf":21,
 "music":{"style":"soft","bpm":76,"gain":0.3},"sfx_vary":True,"sfx_gain":0.42,"phases":9,
 "lines":[{"text":t,"spec":s} for t,s in L]}
json.dump(cfg,open('project.json','w'),ensure_ascii=False,indent=1)
w=sum(len(t.split()) for t,_ in L);print(len(L),'lines',w,'words ~',round(w/173,1),'min speech')
print('images:',sorted({s['img'] for _,s in L}))
