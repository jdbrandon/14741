import socket
import socks
import datetime
import urllib
from stem import Signal
from stem.control import Controller
import stem.process
from stem.util import term

def getaddrinfo(*args):
   return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

def query(url):
   try:
      return urllib.urlopen(url).read()
   except:
      return "Unable to reach %s" % url

def test():
   #countries = ['{ad}', '{ae}', '{af}', '{ag}', '{ai}', '{al}', '{am}', '{an}', '{ao}', '{aq}', '{ar}', '{as}', '{at}', '{au}', '{aw}', '{az}', '{ba}', '{bb}', '{bd}', '{be}', '{bf}', '{bg}', '{bh}', '{bi}', '{bj}', '{bl}', '{bm}', '{bn}', '{bo}', '{br}', '{bs}', '{bt}', '{bw}', '{by}', '{bz}', '{ca}', '{cc}', '{cd}', '{cf}', '{cg}', '{ch}', '{ci}', '{ck}', '{cl}', '{cm}', '{cn}', '{co}', '{cr}', '{cu}', '{cv}', '{cx}', '{cy}', '{cz}', '{de}', '{dj}', '{dk}', '{dm}', '{do}', '{dz}', '{ec}', '{ee}', '{eg}', '{eh}', '{er}', '{es}', '{et}', '{fi}', '{fj}', '{fk}', '{fm}', '{fo}', '{fr}', '{ga}', '{gb}', '{gd}', '{ge}', '{gh}', '{gi}', '{gl}', '{gm}', '{gn}', '{gq}', '{gr}', '{gt}', '{gu}', '{gw}', '{gy}', '{hk}', '{hn}', '{hr}', '{ht}', '{hu}', '{id}', '{ie}', '{il}', '{im}', '{in}', '{io}', '{iq}', '{ir}', '{is}', '{it}', '{je}', '{jm}', '{jo}', '{jp}', '{ke}', '{kg}', '{kh}', '{ki}', '{km}', '{kn}', '{kp}', '{kr}', '{kw}', '{ky}', '{kz}', '{la}', '{lb}', '{lc}', '{li}', '{lk}', '{lr}', '{ls}', '{lt}', '{lu}', '{lv}', '{ly}', '{ma}', '{mc}', '{md}', '{me}', '{mf}', '{mg}', '{mh}', '{mk}', '{ml}', '{mm}', '{mn}', '{mo}', '{mp}', '{mr}', '{ms}', '{mt}', '{mu}', '{mv}', '{mw}', '{mx}', '{my}', '{mz}', '{na}', '{nc}', '{ne}', '{ng}', '{ni}', '{nl}', '{no}', '{np}', '{nr}', '{nu}', '{nz}', '{om}', '{pa}', '{pe}', '{pf}', '{pg}', '{ph}', '{pk}', '{pl}', '{pm}', '{pn}', '{pr}', '{pt}', '{pw}', '{py}', '{qa}', '{ro}', '{rs}', '{ru}', '{rw}', '{sa}', '{sb}', '{sc}', '{sd}', '{se}', '{sg}', '{sh}', '{si}', '{sj}', '{sk}', '{sl}', '{sm}', '{sn}', '{so}', '{sr}', '{st}', '{sv}', '{sy}', '{sz}', '{tc}', '{td}', '{tg}', '{th}', '{tj}', '{tk}', '{tl}', '{tm}', '{tn}', '{to}', '{tr}', '{tt}', '{tv}', '{tw}', '{tz}', '{ua}', '{ug}', '{us}', '{uy}', '{uz}', '{va}', '{vc}', '{vg}', '{vi}', '{vn}', '{vu}', '{wf}', '{ws}', '{ye}', '{yt}', '{za}', '{zm}', '{zw}']
#Initially used the above verbose list of countries, ran the script once and found that these countries produce
#either forbidden messages or have access to the page
   countries = ['{ar}', '{at}', '{au}', '{ba}', '{be}', '{bg}', '{br}', '{ca}', '{ch}', '{cl}', '{cn}', '{cz}', '{de}', '{dk}', '{ee}', '{es}', '{fr}', '{gr}', '{hk}', '{hr}', '{hu}', '{id}', '{ie}', '{il}', '{in}', '{is}', '{it}', '{jp}', '{kr}', '{lt}', '{lu}', '{lv}', '{md}', '{mx}', '{my}', '{nl}', '{no}', '{nz}', '{pa}', '{ph}', '{pl}', '{ro}', '{rs}', '{ru}', '{sg}', '{si}', '{tw}', '{us}',  '{vn}']
   SOCKS_PORT = 7000
   socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
   socket.socket = socks.socksocket

   socket.getaddrinfo = getaddrinfo
   for country in countries:
      print country
      try:
         tor = stem.process.launch_tor_with_config(
            config = {
               'SocksPort': str(SOCKS_PORT),
               'ExitNodes': country
            }
         )
         data = query("http://dogo.ece.cmu.edu/tor-homework/secret")
         print data
         print datetime.datetime.now()
      except OSError:
         continue
      tor.kill()

test()
