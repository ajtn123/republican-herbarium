import data from '../data/calendar.json';

// The complementary days form a thirteenth browsing group, not a historical month.
// Both ordinary and complementary day pages use the same circular reading order.
export const dayGroups = [
  ...data.months.map(month => ({
    label: month.zh,
    href: `/months/${month.slug}/`,
    days: data.days.filter(day => day.month === month.id).map(day => ({
      label: day.zh,
      href: `/days/${day.slug}/`,
    })),
  })),
  {
    label: '补充日',
    href: '/festivals/',
    days: data.festivals.map((festival, index) => ({
      label: `${festival.zh}节${index === 5 ? '（闰年）' : ''}`,
      href: `/festivals/${festival.slug}/`,
    })),
  },
];

const entries = dayGroups.flatMap(group =>
  group.days.map(day => ({ ...day, group }))
);

export function getDayNavigation(href: string) {
  const index = entries.findIndex(entry => entry.href === href);
  if (index === -1) throw new Error(`Unknown calendar day: ${href}`);
  return {
    previous: entries[(index + entries.length - 1) % entries.length],
    group: entries[index].group,
    next: entries[(index + 1) % entries.length],
  };
}
