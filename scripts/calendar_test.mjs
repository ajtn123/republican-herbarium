import assert from 'node:assert/strict';
import {fromGregorian,startOfYear,isLeap,DAY_MS} from '../src/lib/calendar.ts';
for(const [civil,y,m,d] of [['1792-09-22',1,1,1],['1793-10-05',2,1,14],['1793-11-24',2,3,4],['1794-07-27',2,11,9],['1795-09-22',3,13,6],['1799-11-09',8,2,18],['1805-12-31',14,4,10]]){const r=fromGregorian(new Date(civil+'T00:00:00Z'));assert.deepEqual([r.year,r.month,r.day],[y,m,d],civil)}
let n=0;for(let stamp=Date.UTC(1792,8,22);stamp<=Date.UTC(2100,11,31);stamp+=DAY_MS){const date=new Date(stamp),r=fromGregorian(date);assert.equal(startOfYear(r.year)+r.ordinal*DAY_MS,stamp);assert.ok(r.month>=1&&r.month<=13);assert.ok(r.day>=1&&r.day<=(r.festival?(isLeap(r.year)?6:5):30));n++}console.log(`Calendar: seven historical anchors and ${n} daily round trips passed.`);
