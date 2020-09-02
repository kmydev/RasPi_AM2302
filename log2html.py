# -*- coding: utf-8 -*-

import os
from datetime import datetime

row_t = '<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td></tr>'

srcd = '/home/pi/SensorScripts/Log/'
fdate = datetime.now().strftime("%Y%m%d")
#fdate = '20200901'

if __name__=='__main__':
    fname = '{0}{1}.log'.format(srcd, fdate)

    print('<html><head><title>{0}</title></head>'.format(fdate))
    print('<body>')
    print('<p>Last Update: {0}</p>'.format(datetime.now().strftime("%Y/%m/%d %H:%M")))
    print('<table>')
    print(row_t.format('DATE', 'TIME', 'LOGKIND', 'TEMP', 'HUM', 'DETAIL'))

    f = open(fname, 'r')
    for line in f:
        arr = line.strip().split(' ')
        s = row_t.format(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5])
        print(s)
    f.close()

    print('</table></body></html>')

