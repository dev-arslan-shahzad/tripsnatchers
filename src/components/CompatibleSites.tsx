import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "./ui/hover-card";
import { Info } from "lucide-react";

// Array of compatible websites with their URLs
const COMPATIBLE_WEBSITES = [
  {
    name: "LoveHolidays",
    url: "https://www.loveholidays.com"
  },
  {
    name: "TUI",
    url: "https://www.tui.co.uk"
  },
  {
    name: "Jet2Holidays",
    url: "https://www.jet2holidays.com"
  },
  {
    name: "OnTheBeach",
    url: "https://www.onthebeach.co.uk"
  },
  {
    name: "FirstChoice",
    url: "https://www.firstchoice.co.uk"
  },
  {
    name: "BritishAirways Holidays",
    url: "https://www.britishairways.com/travel/home/public/en_gb"
  },
  {
    name: "easyJet Holidays",
    url: "https://holidays.easyjet.com"
  }
];

export function CompatibleSites() {
  return (
    <HoverCard>
      <HoverCardTrigger asChild>
        <button className="flex items-center space-x-1 text-foreground hover:text-primary transition-colors duration-300">
          <Info className="h-4 w-4" />
          <span>Compatible Sites</span>
        </button>
      </HoverCardTrigger>
      <HoverCardContent className="w-64">
        <div className="space-y-2">
          <h4 className="text-sm font-semibold">Compatible Holiday Websites</h4>
          <div className="text-sm text-muted-foreground">
            <ul className="space-y-1">
              {COMPATIBLE_WEBSITES.map((site) => (
                <li key={site.name}>
                  <a
                    href={site.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-primary transition-colors duration-300"
                  >
                    {site.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </HoverCardContent>
    </HoverCard>
  );
}
