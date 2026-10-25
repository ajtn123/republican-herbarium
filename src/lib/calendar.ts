export const DAY_MS=86400000;
export const epoch=Date.UTC(1792,8,22);
export const startOfYear=(year:number)=>epoch+(365*(year-1)+Math.floor(year/4))*DAY_MS;
export function fromGregorian(date:Date){
 const stamp=Date.UTC(date.getUTCFullYear(),date.getUTCMonth(),date.getUTCDate());
 let year=date.getUTCFullYear()-1791;
 while(stamp<startOfYear(year))year--;
 while(stamp>=startOfYear(year+1))year++;
 const ordinal=Math.floor((stamp-startOfYear(year))/DAY_MS);
 return {year,month:Math.floor(ordinal/30)+1,day:ordinal%30+1,ordinal,festival:ordinal>=360};
}
export const isLeap=(year:number)=>year%4===3;
export function roman(n:number){let s=''; for(const [v,c] of [[1000,'M'],[900,'CM'],[500,'D'],[400,'CD'],[100,'C'],[90,'XC'],[50,'L'],[40,'XL'],[10,'X'],[9,'IX'],[5,'V'],[4,'IV'],[1,'I']] as [number,string][]){while(n>=v){s+=c;n-=v;}}return s;}
