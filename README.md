# Russian vessel behaviour at the North Sea

This repository contains code used for research into the behaviour of Russian vessels in the North Sea. The following datasets have been used:

1. Historical AIS data from [Global Fishing Watch](https://globalfishingwatch.org)
2. Historical vessel data from Equasis (ownership, classifications, inspections, etc.)
3. Company information from public sources, e.g. Russian company registry
4. Information provided by North Sea countries authorities
5. Data from [Marine Vessel Traffic](https://www.marinevesseltraffic.com/2013/04/marine-traffic.html) for the identy and positions of NATO vessels.
6. Data from MapStand and EMODnet for infrastructure, like power cables, pipelines and telecommunication cables. 

## Main steps in investigation

1. Get a list of vessels sailing under Russian flag which have been active in the waters of the North Sea countries from 2014 until March 2024. Active means: fishing, port visits, loitering. These events are identified by Global Fishing Watch and can be collected with the GFW API.
2. Create a list of Russian vessels that have been named in reports from NGOs, governments and media in connection with greyzone activities or that have been sanctioned or are owned by a sanctioned company.
3. Collect geo-information on infrastructure in the North Sea, like pipelines, telecommunication and power cables. 
4. Collect information on NATO vessels and their whereabouts using Global Fishing Watch and Marine Vessel Traffic. 
5. Collect information on sensitive NATO objects in Belgium and the Netherlands and convert them to proper geographies. 
6. Manually collect vessel track data of ca 100 vessels that are connected to suspicious entities and have frequented NL and BE waters. 
7. Calculate distance between loitering events and infrastructure lines and points.
8. Calculate AIS gaps in vessel track data.
9. Manually inspect vessel track data for anomalies. 
10. Validate using other data sources (e.g. Danish AIS data and experts)

## Limitations of the data

The data are AIS signals collected from terrestrial and satellite AIS providers and distributed through GFW. AIS coverage can be very patchy. The center of the North Sea has limited coverage. Certainly until around 2019-2020 there were many gaps in the coverage and therefore things went unseen. Later, with the advent of satellite AIS, the coverage became better, but in busy maritime environments AIS signals can cancel each other out, leading to signal loss. It's very hard to distinguish accidental loss from deliberate AIS off switching or manipulation. There were also some problems with data quality of GFW AIS signals, leading to false positives. 

We've looked at loitering events, but it's important to note that the process of finding loitering events is an algorithmic one, where choices have been made about parameters and thresholds. More information can be found at Global Fishing Watch. Some events we found manually weren't flagged as loitering by GFW, probably because the vessel speed was above a certain threshold.

And most importantly, loitering or owernship by a suspicious company is not evidence of wrongdoing. It only strenghtens a suspicion, nothing more and nothing less. So be careful when drawing conclusions from this kind of data and make sure to verify your findings with other sources. 
