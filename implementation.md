	
# 7 Implementation Notes
	
The following section will provide brief notes on how certain objects and fields are to be interpreted and implemented.
	
## 7.1 No-Bid Signaling
	
This section covers best practices for using the optional no-bid signaling. See the List: No-Bid Reason Codes in OpenRTB 3.0 <#_2rrrqc1>for the enumerated list of no-bid reason codes.
	
Many exchanges support multiple response types as a no-bid:
	
- HTTP 204 “No Content” from the bidder (most economical in terms of bandwidth).
- An empty JSON object:
 	{}
- A well-formed no bid response:
 	{"id": "1234567890", "seatbid": []}
- A well-formed no bid response with a reason code:
 	{"id": "1234567890", "seatbid": [], "nbr": 2}
	
An important issue in RTB is when impressions are triggered by software robots mimicking web browsers. Such robots may be implicitly or explicitly driving these false transactions. The following represents a set of symmetric best practices for exchanges and bidders to help recognize and reject these events.
	
*Responsibility of the exchange*
	
Make best effort to classify and reject “non-human traffic” requests for ads to the exchange via the following best practices:
	
- (Recommended) Filter impressions from known spiders via user-agent classification.
- (Recommended) Filter impressions from suspected NHT via a “detector”.
	
*Responsibility of the bidder*
	
- (Recommended) no-bid impressions from known spiders via user-agent classification.
- (Recommended) no-bid impressions from suspected NHT via a “detector”.
- Specify a no-bid reason code in either case.
	
*Where:*
	
- For exchanges, filtering the impression means that the exchange should respond to the “ad call” with either a blank HTTP 204 response or an unpaid ad (PSA) and not offered to any bidders.
- For bidders, filtering the impression means that the bidder should respond with a no-bid.
- For both exchanges and bidders, the impression transaction records should be clearly marked in any logging systems and be removed from contributing to any event counts associated with planning, forecasting, and reporting systems.
	
## 7.2 Impression Expiration
	
Recapping the typical impression flow through RTB, an ad will be requested by a client (e.g., web browser, mobile app or an SDK therein) possibly through other server intermediaries, and ultimately to the RTB exchange. The exchange conducts an auction among buyers who bid with a proposed price, possibly markup for use if the bid wins (markup can also be delivered on the win notice itself), and other metadata about the bid. The exchange then selects a winner, issues a win notice to the winning bidder, and passes the markup back to the client.
	
Winning the auction, however, does not guarantee that the ad will be successfully delivered to the client or that it will meet viewability expectations. Furthermore, policies vary among exchanges as to the criteria for billing. Most consider an ad billable upon some form of delivery or rendering vs. the auction win alone. This aligns better with the buyer’s obvious goal of ensuring that the impressions they pay for are actually displayed.
	
Some exchanges attempt to facilitate this alignment by placing the win notice in the winning ad markup so that it can serve as both a win notice and rendering notice. This is neither endorsed nor prohibited by OpenRTB except that it precludes the exchange from accepting markup on the win notice return as described in Section 4.3.1. Similarly, many buyers use their own tracking URL placed within their ad markup to signal rendering independent of the OpenRTB auction win notice. In video specifically, VAST supports an impression tracking URL that is often used for billing and is always distinct from the auction win notice.
	
To abstract the concept, let us refer to “billing notice” as the firing of some notification URL at the time when the clearing price of the impression will be booked as spend. This is irrespective of whether the actual OpenRTB win notice URL is delegated to the client for firing or some other tracking URL is used.
	
For buyers, this billing notice is used to book progress toward spend goals and frequency caps and drive pacing algorithms. When the billing notice is delayed significantly, these critical functions can be seriously impaired. There are legitimate reasons for some delays such as caching. A common scenario is a video interstitial impression in a mobile app. Refining the example, consider a game where the video is prefetched during game play so that it can be shown after the current game level ends. This is important for the user experience but can delay the rendering of the ad for many minutes.
	
Bidders are strongly advised to track the time between the auction and the win and/or billing notices to ensure reasonable delays. If unreasonable delays are encountered frequently, bidders may elect to ignore such events and bring them to the attention of the exchange for resolution. Unfortunately, the sequence from ad request through the auction and finally to rendering and billing is fundamentally not transactional. There are simply too many parties, policies, and technologies involved and thus a good support relationship between exchange and buyer is still important.
	
The OpenRTB protocol does provide some real-time assistance, however. The imp.exp attribute (Section 3.2.4) in the bid request allows an exchange to provide guidance to bidders of the number of seconds that may elapse between the auction and the billing event. As usual, omitted means unknown. Bidders can then decide if they want to bid understanding the likely delay. Bidders are advised, however, to interpret this as guidance as opposed to a contract unless the exchange expresses otherwise since exchanges are not always in a position to make hard guarantees (e.g., the SDK within the client app may not be under the exchange’s control).
	
Similarly, the bid.exp attribute (Section 4.2.3) in the bid response allows the bidder to express the maximum number of seconds they are willing to tolerate between auction and billing notice. This allow the exchange to drop bids with expiration constraints it believes are likely to be violated. Bidders should not assume that a delayed billing notice greater than their specified bid expirations will not be billable. That is a policy and contract discussion between bidder and exchange and not imposed by OpenRTB.
	
The following expiration times are offered as examples of reasonable delays based on the nature of the impression. These are only provided as rules of thumb. A more data-driven method of determining these times in specific situations is highly recommended.
	
- Desktop and mobile web browsers: 1 Minute
- Mobile app banner ads that may be cached: 5 Minutes
- Mobile app native ads that may be cached: 10 Minutes
- Mobile and video interstitials: 30 Minutes (or even longer)
- Audio or video with server-side stitching: Very Long or Unknown
	
## 7.3 PMP & Direct Deals
	
**Best Practice Bidding Logic**
	
Receive request and parse;
Create empty bid list for response;
If request contains the impression[].pmp object; match bids against each pmp.deals[];
enforce targeting for dealID and seatID; append best M matching bids to response;
If pmp.private_auction = False;
match open auction bids against the request; append top N bids by price to response;
Return response list to exchange;
	
*Recommendations*
- M >= 1, preferably one per matching Deal ID.
- N >= 2 to assist with blocking rate issues.
- Minimum viable is “1+1” bidding.
- Ideal is “M+N” bidding.
	
**Warning**
	
Returning only one bid when both Deal ID and open auction bids are valid creates problems. The exchange side may be configured by a publisher to prioritize all Deal ID bids above open auction bids, or to force a price auction between them with different floors by class of bid. There are multiple common practices that depend on how the publisher prefers to sell inventory with Deal ID.
	
**Policy Recommendations**
	
- A Deal ID should be utilized for any situation where the auction may be awarded to a bid not on the basis of price alone. Any prioritization of bids other than by price should have a Deal ID.
- A Deal ID is recommended for all situations where a preferential floor may be assigned to a seat entity.
	
**Anti-Patterns**
	
The below is a set of anti-patterns that OpenRTB supporting platforms have observed in various attempts to implement Deal ID bidding logic.
	
**Subjecting Deal ID Bids to an internal auction on price**
	
The ideal bidding logic describes a process of being liberal about sending bids. Deal ID bids may not be subject to a classic price auction. There may be an expectation that the buyer and seller want prioritization to achieve a larger objective: complete delivery of the Deal represented by the Deal ID. Thus any bidding logic that sorts Deal ID bids by price (with or without open marketplace bids) and truncates the list too aggressively can endanger the fulfillment of the Deal.
	
**Associating Deal ID to the wrong Object**
	
A Deal ID should be treated as a “targeting token” associated to orders, line-items or campaigns. If the Deal ID is associated to a Seat/Buyer it may create an undesired application of the Deal ID too many active campaigns. Alternatively if it is associated to the Advertiser it may limit that entity to only a single Deal ID.
	
**Improper Handling of the Private vs Open Market Flag**
	
The pmp.private_auction flag indicates that the seller is willing or not willing to accept open market bids (i.e., “all bidders are welcome”). If this flag is not read and interpreted correctly, bid responses may be invalid. Open market bids sent to a private impression auction may be rejected and should not have been exposed to all bidders.
	
**Improper handling of Seat IDs**
	
If Seat IDs are treated as a filter of eligible demand partners on an open market impression, this defeats the “all bidders are welcome” intention.
	
**Silently Applying Margin Discounts to Deal ID Bids**
	
With Deal ID buyers are sellers are communicating directly. The Exchange and Bidder become third- party automation platforms. If there are any automatic or silent discounts of bid prices (based upon margins or fees) set by either the exchange or the bidder, then the Deal may fail to function correctly.
	
**Use cases**
	
*Case-1: Open Trading Agreement with Buyer*
	
- Between publisher and buying entity.
- Publisher sets an access rule defining the price floor for a specific buyer.
- Locked to the buyer.
- Broadcast price floor.
- Public/open inventory.
- No Deal ID needed (Deal ID is optional).
- No named advertiser(s).
- No prioritization of bids.
- Daily total or frequency caps optional on publisher/exchange side.
- All placements or limited to specific placements.
- Targeting is up to the buyer/bidder.
	
*Case-2: Open Trading Agreement with Buyer with Named Advertisers*
	
- As Case-1 with a list of named advertisers.
	
*Case-3: Open Bidding with Deal ID as Value-added Markers*
	
- Between publisher and buying entity.
- Publisher sets a price floor for URL masked inventory.
- Public/open inventory (i.e., all buyers welcome).
- Deal ID represents “Package Tokens”.
- Each Deal ID signals that the impression falls into various content and placement categories.
- Floor is associated to each Deal ID to signal cost for usage of that token.
- Winner is decided by bid price.
- Execution of targeting is up to the buyer/bidder.
	
*Case-4: First Look Trading Agreement*
	
- Between publisher and buying entity.
- Publisher sets an access rule defining the price floor for the buyer.
- Locked to the buyer.
- Known price floor.
- Deal ID needed.
- Optional named advertiser list.
- Prioritization of bids expected.
- Daily total or frequency caps optional on publisher/exchange side.
- All placements or limited to specific placements.
- Targeting is up to the buyer/bidder.
	
*Case-5: Direct Option Deal with Advertiser via RTB*
	
- Between Publisher and Advertiser or their representative.
- Publisher sets a rule defining a price floor and prioritization for specific advertiser(s).
- Fill rate is expected to be greater than or equal to X%.
- Locked to the buyer.
- Private/exclusive inventory.
- Limited to a set list of advertiser names (generally variants of one name).
- Known price floor.
- Deal ID needed.
- Prioritization of bids expected.
- Daily total or frequency caps will apply on bidder side; optional on Exchange side.
- Limited to specific placements.
- Targeting is mostly enforced by buyer/bidder.
	
*Case-6: Direct Option Deal with Advertiser via RTB with Private Data*
	
- Same as Case-4.
- Deal ID represents some combination of private first-party data from the Publisher.
	
*Case-7: Full-Fill Direct Deal with Advertiser via RTB*
	
- Same as Case-4.
- Fill rate is expected to be 100% or nearly so.
	
*Case-8: Full-Fill Direct Deal with Advertiser via RTB with Private Data*
	
- Same as Case-6.
- Deal ID represents some combination of private first-party data from the Publisher.
	
## 7.4 Skippability
	
This section clarifies the common use cases related to declaring skippability of video creatives.
	
Under most circumstances for RTB transactions, publishers and exchanges prefer to control the ability to skip the ad. OpenRTB therefore assumes by default that a standard linear video ad can be used as the
response to a skippable request and the ability to skip the ad will be provided by the supplier’s player automatically.
	
The presence of the video.skip attribute in the bid request with a value of “1” should be assumed to mean that the publisher will impose a skip button on the ad. The absence of the video.skip attribute should be assumed to mean that it is unknown whether the publisher will impose a skip button.
	
DSPs should confirm with publishers whether it is permissible to respond with ads that provide their own skip functionality (e.g., using VPAID to render a skip button). If bidding with such an ad and only if doing so, the bid must indicate creative attribute “16” using the attr array in the bid response.
	// add note on page 70
	
Some examples of these concepts follow:
	
**Bid Request** 
	
*Case-1: Skippable after N Seconds for All Creatives*
	
In this case, the publisher will impose skippability. All ads will be skippable, but only after 5 seconds of play. Creatives with a total duration of 5 seconds or less would not be skippable since they would never reach this threshold.
	
"video": {
	
..., "skip": 1, "skipafter": 5, ...
	
}
	
*Case-2: Skippable after N Seconds for Minimum Duration Creatives*
	
In this case, the publisher will impose skippability. However, only creatives with a total duration greater than 15 seconds will be skippable. For ads that satisfy this minimum total duration, skippability is enabled after 5 seconds of play. Note that although these values are integers, they will compare as precise values with actual video durations. For example, a video with duration 15.1 seconds does satisfy a skipmin value of 15 (i.e., think of the skipmin value as being 15.0).
	
"video": {
	
..., "skip": 1, "skipmin": 15, "skipafter": 5, ...
	
}
	
*Case-3: Non-Skippable unless Requested by the Ad Markup*
	
In this case, the publisher will not impose skippability. Ads will only be skippable if requested by the ad markup. This is supported by VPAID and VAST 3.0, for example.
	
"video": {
	
..., "skip": 0, ...
	
}
	
*Case-4: Unknown Skippability*
	
In this case, the skip attribute is omitted which indicates that exchange does not know if skippability will be imposed by the publisher. This may be the case, for example, when the exchange is not an SSP and thus may not have control or full knowledge of the publisher’s intentions.
	
**Bid Response**
	
Consider Case-3 above, where the publisher does not impose skippability. If the ad markup itself will request skippability (e.g., via VPAID or VAST 3.0), then the bid must signal this intention. This is accomplished by including creative attribute 16 (i.e., Skippable) in the bid as shown below. If the markup is not going to request skippability, then this creative attribute should not be indicated.
	
When responding to Case-3 with this skippable attribute specified in the bid, the publisher should provide skippability either by instructing the VAST 3.0 player to activate skippability (refer to the VAST
3.0 “skipoffset” attribute) or by allowing the ad to render its own skip button using VPAID.
	
"bid": {
	
..., "attr": [16], ...
	
}
	
In Case-1 and Case-2 where the publisher may impose its own skippability, creative attribute 16 should not be specified. Furthermore, publishers are advised to filter responses containing attribute 16 since this could conflict with the skip button rendered by the publisher. When using a VAST 3.0 response, publishers may choose to implement support for VAST 3.0 “skipoffset” at their discretion and ads should be assumed to play non-skippable if the player does not support it.
	
## 7.5 Regs Resources
	
The regs object contains any legal, governmental, or industry regulations that the sender deem applicable to the request.
	
Please see the below resources for more details and framework specifications should you choose to implement them:
	
**GDPR (General Data Protection Regulation)**
https://github.com/InteractiveAdvertisingBureau/GDPR-Transparency-and-Consent-Framework

**CCPA (California Consumer Privacy Act)**
https://github.com/InteractiveAdvertisingBureau/USPrivacy

## 7.6 Pod Bidding for Video and Audio
	
Starting in version 2.6, OpenRTB now supports ‘pod bidding’ for video and audio content streams.
An ad pod is the term describing an ad break of the type you’d see in a TV-like viewing experience or hear on a radio stream. An ad pod typically contains one or more in-stream creative assets that play out contiguously within a stream of video or audio content. Ad podding features in OpenRTB 2.6 build on capabilities in previous versions for including multiple ad requests within a single bid request object to indicate those ad requests are in some way related. Pod bidding signals communicate additional information about the pod & impression opportunities within the pod such as the sequence of the ad impressions, total pod length, maximum # of ads within a pod, multiple pod associations, and more.
	
**Terminology**
	
Ad Slot: Space for an individual ad impression within a pod.
	
Structured Pod: The seller offers a fully defined pod structure; the number of ad slots, their slot in the ad pod, and duration is pre-defined and static.
	
	//insert photo on page 73
	
Dynamic Pod: The seller offers a pod structure where the number of ads & the duration of each ad in the break is indeterminate, but the total duration and maximum number of ads are constrained. In other words, the total duration of the pod is known, but the number and durations of the individual ads within the break may not be defined ahead of time. This allows bidders more flexibility to optimize their selection of ads across the demand on their platform.
	
	//insert photo on page 74
	
Hybrid Pod: The seller offers a pod structure containing BOTH structured and dynamic components. In other words, the ad pod is composed of some combination of ad slots with predetermined durations, and ad slots constrained by a total duration & maximum number of ads.
	
**Recommendations**
	
- Sellers should only indicate a slotinpod of 1, 2, or -1 if they can absolutely guarantee placement of an ad within the first or last slot of an ad pod.
- Buyers should only indicate a slotinpod in response to a dynamic pod segment, including a dynamic component of a hybrid pod, if they only want to buy the first or last ad slot specifically
- Note that buyers should *only* return a slotinpod value in response to a Dynamic portion of a pod.
- Buyers should avoid using the slotinpod field in bid responses for structured pods, or the structured components of hybrid pods, because the impid field already uniquely identifies the ad slot.
- Buyers should look for mincpmpersec when available, otherwise fall back to bidfloor
- Sellers should include either the required durations field (communicating exact durations) OR the max & min duration fields, but not both.
- Sellers are encouraged to include the maxseq field when offering a dynamic pod with a pod duration
- Sellers are encouraged to offer dynamic pods when possible to allow bidders to source the most optimal demand from their platforms
- Buyers should expect that final pod construction is done by the seller. Buyers who submit N bids for a particular pod may find that the seller selects anywhere between 0 to N of those bids to construct the pod that is shown to the user. Furthermore, the seller may co-mingle bids from other buyers in that pod.

**Pod bidding example scenarios**
	
*“Structured” Ad Pod Request/Response*
	
This scenario illustrates an example where the bid request contains 2 structured ad pods, and the response corresponds to the first positions in each of the 2 signaled pods.
	
**BidRequest**
	
{ "imp": 
	
	[{ "id": "1", 
	
	"video": { 
	
		"podid": "pod_1", 
	
		"podseq”: 1, 
	
		"slotinpod": 1, 
	
		"mimes": [ 
	
			"video/mp4", 
	
			"video/ogg", 
	
			"video/webm" 
	
		], 
	
		"linearity": 1, 
	
		"maxduration": 60, 
	
		"minduration": 0, 
	
		... 
	
	}, "exp": 7200, 
	
	"bidfloor": 8, 
	
	"bidfloorcur": "USD", 
	
	}, 
	
	{ 
	
		"id": "2", 
	
		"video": { 
	
			"podid": "pod_1", 
	
			"podseq": 1, 
	
			"slotinpod": 0, 
	
			"mimes": [ 
			
				"video/mp4", 
	
				"video/ogg", 
	
				"video/webm" 
			], 
			"linearity": 1, 
			
			"maxduration": 30, 
	
			"minduration": 0, 
	
			... 
	
		}, 
	
		"exp": 7200, 
	
		"bidfloor": 8, 
	
		"bidfloorcur": "USD", 
	
		...
	
	}, 
	
	{ 
	
		"id": "3", 
	
		"video": { 
	
			"podid": "pod_2", 
	
			"podseq": 0, 
	
			"slotinpod": 1, 
	
			"mimes": [ 
	
				"video/mp4", 
	
				"video/ogg", "
	
				video/webm" 
	
			], 
	
			"linearity": 1, 
	
			"maxduration": 30, 
	
			"minduration": 
	
			0, 
	
			... 
	
		}, 
	
		"exp": 7200, 
	
		"bidfloor": 8, 
	
		"bidfloorcur": "USD", 
	
		... 
	
		}, 
	
		{ 
	
			"id": "4", 
	
			"video": { 
	
				"podid": "pod_2", 
	
				"podseq": 0, 
	
				"slotinpod": 0, 
	
				"mimes": [ 
	
					"video/mp4", 
	
					"video/ogg", 
	
					"video/webm" 
	
				], 
	
				"linearity": 1, 
	
				"maxduration": 60, 
	
				"minduration": 0, 
	
				... 
	
			},
	
			"exp": 7200, 
	
			"bidfloor": 8, 
	
			"bidfloorcur": "USD", 
	
			... 
	
		} 
	
	], 
	
	... 
	
}

	
	
**BidResponse**
	
{ 
	
	"id": "9b9ee818a85d948d5231ffe839a9729a", 
	
	"seatbid": [{ 
	
		"bid": [{
	
			"id": "1", 
	
			"impid": "1", 
	
			"price": 0.27, 
	
			"adid": "123456", 
	
			"adm": "<?xml version=\"1.0\" encoding=\"UTF-8\"?><VAST version=\"2.0\"> ...", 
	
			"adomain": [ 
	
				"advertiserA.com" 
	
			], 
	
			"cid": "456789", 
	
			"crid": "123456", 
	
			"dur": 30 
	
		}], 
	
		"seat": "1"
	
	}, 
	
	{ 
	
		"bid": [{ 
	
			"id": "2", 
	
			"impid": "3", 
	
			"price": 0.27, 
	
			"adid": "234567", 
	
			"adm": "<?xml version=\"1.0\" encoding=\"UTF-8\"?><VAST version=\"2.0\"> ...", 
	
			"adomain": [ 
	
				"advertiserB.com" 
	
			], 
	
			"cid": "567890", 
	
			"crid": "234567", 
	
			"dur": 15 
	
		}], 
	
		"seat": "2" 
	
	} 
	
	], "cur": "USD" }
	
	
*“Dynamic” Ad Pod Request/Response*
	
This scenario illustrates an example where the bid request contains 1 dynamic pod, the publisher can guarantee delivery against the first or last slot, and the response contains 3 bids from 3 different advertisers, for the signalled pod. The first bid in the response is only eligible for the first position in the pod.
	
BidRequest

{

	"imp": [{
	
		"id": "1",
		
		"video": {
		
			"podid": "preroll_pod",
			
			"mimes": [
			
				"video/mp4",
				
				"video/ogg",
				
				"video/webm"
				
			],
			
			"linearity": 1,
			
			"maxduration": 60,
			
			"minduration": 0,
			
			"maxseq": 4,
			
			"poddur": 60,
			
			"slotinpod": 2,
			
			...
			
		},
		
		"exp": 7200,
		
		"bidfloor": 8,
		
		"bidfloorcur": "USD",
		
		...
		
	}],
	
	...
	
}



BidResponse

{

	"id": "9b9ee818a85d948d5231ffe839a9729a",
	
	"seatbid": [{
	
			"bid": [{
			
				"id": "1",
				
				"impid": "1",
				
				"price": 0.27,
				
				"adid": "123456",
				
				"adm": "<?xml version=\"1.0\" encoding=\"UTF-8\"?><VAST version=\"2.0\"> ...",
				
				"adomain": [
				
					"advertiserA.com"
					
				],
				
				"cid": "456789",
				
				"crid": "123456",
				
				"slotinpod": 1,
				
				"dur": 30
				
			}],
			
			"seat": "1"
			
		},
		
		{
		
			"bid": [{
			
				"id": "2",
				
				"impid": "1",
				
				"price": 0.27,
				
				"adid": "234567",
				
				"adm": "<?xml version=\"1.0\" encoding=\"UTF-8\"?><VAST version=\"2.0\"> ...",
				
				"adomain": [
				
					"advertiserB.com"
					
				],
				
				"cid": "567890",
				
				"crid": "234567",
				
				"dur": 15
				
			}],
			
			"seat": "1"
			
		},
		
		{
		
			"bid": [{
			
				"id": "3",
				
				"impid": "1",
				
				"price": 0.27,
				
				"adid": "345678",
				
				"adm": "<?xml version=\"1.0\" encoding=\"UTF-8\"?><VAST version=\"2.0\"> ...",
				
				"adomain": [
				
					"advertiserC.com"
					
				],
				
				"cid": "678901",
				
				"crid": "345678",
				
				"dur": 15
				
			}],
			
			"seat": "2"
			
		}
		
	],
	
	"cur": "USD"
	
}


	
	
*“Hybrid” Ad Pod Request/Response*
	
This scenario illustrates an example where the bid request contains slot 1 in the first impression object and a dynamic pod to fill the duration. The response contains 3 bids from 3 different advertisers, for the signalled pod. The first bid in the response is only eligible for the first position in the pod and the second two responses would be to fill the remainder of the pod.
	

BidRequest

{

	"imp": [{
	
			"id": "1",
			
			"video": {
			
				"podid": "pod_1",
				
				"slotinpod": 1,
				
				"mimes": [
				
					"video/mp4",
					
					"video/ogg",
					
					"video/webm"
					
				],
				
				"linearity": 1,
				
				"maxduration": 15,
				
				"minduration": 15,
				
				...
				
			},
			
			"exp": 7200,
			
			"bidfloor": 15,
			
			"bidfloorcur": "USD",
			
			...
			
		},
		
		{
		
			"id": "2",
			
			"video": {
			
				"podid": "pod_1",
				
	"slotinpod": 0,
	
				"mimes": [
				
					"video/mp4",
					
					"video/ogg",
					
					"video/webm"
					
				],
				
				"linearity": 1,
				
				"maxduration": 60,
				
				"minduration": 0,
				
				"maxseq": 4,
				
				"poddur": 60,
				
	                             ...
				     
			},
			
			"exp": 7200,
			
			"bidfloor": 8,
			
			"bidfloorcur": "USD",
			
			...
			
		}
		
	}],
	
	...
	
}


BidResponse

{

	"id": "9b9ee818a85d948d5231ffe839a9729a",
	
	"seatbid": [{
	
			"bid": [{
			
				"id": "1",
				
				"impid": "1",
				
				"price": 20.27,
				
				"adid": "123456",
				
				"adm": "<?xml version=\"1.0\" encoding=\"UTF-8\"?><VAST version=\"2.0\"> ...",
				
				"adomain": [
				
					"advertiserA.com"
					
				],
				
				"cid": "456789",
				
				"crid": "123456",
				
				"dur": 15
				
			}],
			
			"seat": "1"
			
		},
		
		{
		
			"bid": [{
			
				"id": "2",
				
				"podid": "pod_1",	
				
				"impid": "2",
				
				"price": 9.27,
				
				"adid": "234567",
				
				"adm": "<?xml version=\"1.0\" encoding=\"UTF-8\"?><VAST version=\"2.0\"> ...",
				
				"adomain": [
				
					"advertiserB.com"
					
				],
				
				"cid": "567890",
				
				"crid": "234567",
				
				"dur": 15
				
			}],
			
			"seat": "1"
			
		},
		
		{
		
			"bid": [{
			
				"id": "3",
				
				"podid": "pod_1",
				
				"impid": "2",
				
				"price": 10.27,
				
				"adid": "345678",
				
				"adm": "<?xml version=\"1.0\" encoding=\"UTF-8\"?><VAST version=\"2.0\"> ...",
				
				"adomain": [
				
					"advertiserC.com"
					
				],
				
				"cid": "678901",
				
				"crid": "345678",
				
				"dur": 15
				
			}],
			
			"seat": "2"
			
		}
		
	],
	
	"cur": "USD"
	
}

	
	
## 7.7 Network vs Channel Example Cases
	
Starting in version 2.6, OpenRTB now supports Network and Channel objects. See 3.2.23 and 3.2.24 for details).While these examples are straight forward for traditional linear television, the options for CTV consumption warrant a few examples.
	
Example 1: A user viewing content on an internet connected device, on an app with multiple channel options (e.g. Discovery+ App > HGTV Channel/show)
	
- Discovery is the Network
- HGTV is the Channel
	
Example 2: A user viewing content on an internet connected device, on an app that streams content directly (Roku > Hulu > Hulu Original show)
	
- Hulu is the network (also identified by bundleID)
- Hulu is the channel
	
 Example 3: A user viewing content on an internet connected device, on a device offered channel (Roku > Fubo > Comedy Central show)
	
- Roku is the device
- FuboTV is the network (also identified by bundleID)
- Comedy Central is the channel
	
Example 4: A user is viewing content on an internet connected device, on a device offered channel that licenses content (Samsung TV > Pluto > Pluto TV Spotlight)
	
- Samsung TV is the device
- Pluto is the network (also identified by bundleID)
- PlutoTV Spotlight is the channel
	
## 7.8 Counting Billable Events and Tracked Ads
	
There are multiple conventions for how to count billable events or tracked ads via OpenRTB, typically an impression or other such common metric. This section outlines the common ones, addresses common mistakes, and offers a comparison of the approaches.
	
This section addresses technical methods available for implementers to consume these events. These events have specific business definitions and criteria for counting eligibility set by the Media Rating Council, and implementers should also consult the Media Rating Council’s guidelines.
	
Implementers should discuss the definition of the billable event and the technical basis for counting it with their counterparties to determine a mutually acceptable approach.
	
**Overview of counting methodologies**
	
	//insert table from page 82
	
Method	Remarks
Pixel in markup	Widely supported Normally fired from client-side browser Prone to discrepancies May overcount in some circumstances (i.e. mobile app) Only applicable for display
VAST <Impression> event	Recommended for audio/video Only applicable for audio/video
Billing notice (“burl”)	Best alignment between DSPs and exchanges to count tracked ads Minimal discrepancy Not recommended for audio/video, otherwise applicable to all creative types Usually (and recommended to be) fired server-to-server, but based on an initial client-side event
Native eventtrackers/imptrackers/jstrackers	Only applicable to native ads
	
**Pixel in markup (banner ads)**
	
This is the original convention for counting impressions/tracked ads; in this method, the OpenRTB specification itself does not address how to receive the events. The bidder self-embeds a tracking pixel in their HTML markup (i.e. an <img> tag which makes a request to the bidder’s servers). When the client device loads the markup, it fires the pixel.
	
For banner ads on web, this is a widely adopted approach to counting billable events/tracked ads, however some circumstances arise in which there may be discrepancies. Differences in timing between when an exchange’s and a DSP’s pixel load may result in discrepancies, and the noisy nature of the public Internet and variable connectivity quality of client devices may result in one pixel firing but not the other. Additionally, this method does not address certain scenarios well, namely:
	
- **Mobile apps** – a billable event may only be counted when the ad is displayed. In mobile apps, the markup is often fetched well in advance of being displayed to buffer against slow and unreliable connections. The markup may never be displayed if the user abandons the app before the ad is displayed – especially for interstitials.
	
- **Creative auditing** – markup may be loaded to scan for malvertising, etc., which may generate spurious extra billable/tracked ad events, including for unwon auctions.
	
BEST PRACTICE: When it is possible to do so, exchanges should avoid using adm-based notifications as the determinant for billing events in the mobile app context, and instead use burl or an independent measurement approach (e.g. OMID), that is predicated upon an ad actually being displayed to the user.
	
**VAST <Impression> event (video/audio)**
	
The VAST specification includes a provision for <Impression> objects, which demand chain participants can use to request notifications when a billable event has occurred. The IAB prescribes that for video, the VAST <Impression> event is the official signal that the billable event has occurred.
	
Demand chain participants are discouraged from using billing notice URLs (burl) for video/audio transactions.
	
**Billing notice (“burl”)**
	
Billing notice support was introduced in OpenRTB 2.5. In this scenario, outside of the ad markup itself, a “billing notice URL” is included in the bid response. A billing event is when a transaction results in a monetary charge from the publisher to an exchange, and subsequently from the exchange or other intermediary to one of their demand-side partners. This event is subject to publisher and exchange-specific business policies that should be conveyed clearly to their partners. For a DSP, this event signals that they can increment spend and deduct the remaining budget against the related campaign. The exchange conveys this event by invoking the URL provided by the demand source in the bid.burl attribute.
	
BEST PRACTICE: Firing the billing notice URL represents the fulfillment of a business transaction between a publisher and an exchange, or between the exchange and its demand partner. This should not be delegated to another party including a client-side pixel, although a pixel may be the initiating signal for billing to the exchange.
	
BEST PRACTICE: Exchanges, upon determining that a billable event has occurred (e.g., receipt of client-initiated billable event), and in order to minimize discrepancies between themselves and their demand sources, should invoke the billing notice from the server-side. This should be done as "close" as possible to the moment when the exchange books revenue. See the below section regarding best practices for server-side billing notifications.
	
BEST PRACTICE: Exchanges are highly encouraged to standardize on a client-initiated render or viewability event as the basis for the billing event. This is generally the most consistent approach in a complex supply chain scenario composed of multiple auction decision points.
	
BEST PRACTICE: Publishers should generally refer to the Media Rating Council’s guidelines to determine when the criteria have been met to consider a transaction billable.
	
BEST PRACTICE: The public internet is noisy and this event is financial in nature. If an entity calling a billing notice receives a response other than HTTP 200 or 204, it should consider a retry scheme (e.g., every 10 seconds for the next minute). Conversely, an entity receiving billing notices should endeavor to make their endpoint idempotent to avoid double counting.
	
BEST PRACTICE: When it is possible to do so, exchanges should avoid using adm-based notifications as the determinant for billing events in the mobile app context, and instead use burl or an independent measurement approach (e.g. OMID), that is predicated upon an ad actually being displayed to the user.
	
For VAST video/audio, if the bid.burl attribute is specified, it should be fired at the same time as the VAST <Impression> event. However, subtle technical issues may lead to additional discrepancies and bidders are cautioned to avoid this scenario. One option is for exchanges nearest a video supply source to use the VAST <Impression> event as their billing signal and then use the billing notice URL (burl) as described.
	
**Native eventtrackers, imptrackers, jstrackers**
	
For native ads specifically, the OpenRTB Native specification offers options for including an impression tracking URL or script to be loaded at impression time. See the OpenRTB Native spec for more information. For native video, most platforms utilize the impression events within VAST for billing and other event notifications, rather than the structured tracking options available within the native spec.
	
**Win notice (“nurl”) – not a billable or tracked ad event**
	
At first glance, an auction “win” and the associated win notice (“nurl”) field appears suitable as a proxy for billable/tracked ad counting. However, winning an auction does not guarantee that an impression will indeed be served, and in fact in many cases only a small percentage of won auctions will become impressions. This occurs because of downstream auctions (i.e. client-side header bidding), inability to play back media (in video and audio), etc.
	
**Win notice URLs should never be used to count impressions or tracked ads.**
	
**Best Practices for server-side billing notifications*
	
In some cases, publishers or their vendors may choose to fire impression notifications from a server. This is very common in long-form video, which uses server-side ad insertion to coordinate the delivery and measurement of ads to a “thin” client on the user’s device. It is also common in mobile app, where the monetization SDK uses a server-side service to fire burl notifications.
	
The following best practice is derived from the VAST 4.2 spec (page 17), but recommended for any impression notification (for all formats, regardless of protocol or version).
	
BEST PRACTICE: When possible, exchanges are encouraged to send billing notice URL (burl) notifications from the server-side, to minimize discrepancies with demand partners. The billable event itself should originate from a client-side event per MRC guidelines.
	
BEST PRACTICE: When firing impression notifications via HTTP request from the server-side, the notifier should:
	
- Make use of the X-Forwarded-For or X-Device-IP HTTP header to indicate the IP address of the client device on behalf of which the notification is being sent.
- Make use of the X-Device-User-Agent HTTP header to indicate the UserAgent of the client device on behalf of which the notification is being sent.
	
These HTTP headers allow recipients of impression notifications to run anti-IVT checks using metadata about the end user device, rather than the server itself.
	
BEST PRACTICE: When firing impression notifications via HTTP request from the server-side, the notifier should establish an ads.cert Call Sign and make use of the ads.cert Authenticated Connections protocol to cryptographically sign notifications. This allows recipients of impression notifications, who’ve established ads.cert Call Signs of their own, to authenticate the sender for anti-fraud purposes.
	
# Appendix A. Additional Information
- Creative Commons / Attribution License
 	creativecommons.org/licenses/by/3.0
- IAB (Interactive Advertising Bureau)
 	www.iab.com
- IAB Quality Assurance Guidelines (QAG):
 	www.iab.com/guidelines/iab-quality-assurance-guidelines-qag-taxonomy/
- JavaScript Object Notation (JSON)
 	www.json.org
- MMA (Mobile Marketing Association)
 	mmaglobal.com
- OpenRTB Project on Github
 	github.com/openrtb/OpenRTB/
- Apache Avro
 	avro.apache.org
 	Protocol Buffers (Protobuf)
code.google.com/p/protobuf
- Google Metro Codes
 	code.google.com/apis/adwords/docs/appendix/metrocodes.html
- U.N. Code for Trade and Transport Locations:
 	www.unece.org/cefact/locode/service/location.htm
	
# Appendix B. Specification Change Log
	
This appendix serves as an index of specification changes across 2.x versions. These changes pertain only to the substance of the specification and not routine document formatting, organization, or content without technical impact.
	
**Version 2.5 to 2.6:**
	
	//insert table from page 88
Section	Description
3.2.1 3.2.16 4.2.3 3.2.18	Added new language field to support IETF BCP 47 IETF BCP 47 offers additional layers of granularity, for example, differentiating written language versions of the same spoken language (e.g. Traditional and Simplified Chinese) https://en.wikipedia.org/wiki/IETF_language_tag

5	Removed section (Enumerated Lists) All references now point to AdCOM 1.0 / OpenRTB 3.0 Lists
3.2.1 3.2.13 3.2.14 3.2.15 3.2.16 3.2.17 4.2.3	Objects: BidRequest, Site, App, Publisher, Content, Producer, Bid, Use of cattax for all taxonomy references
3.2.7 3.2.8	Objects: Video, Audio Added rqddurs
3.2.7 3.2.8	Objects: Video, Audio Added maxseq, poddur, podid, podseq, mincpmpersec, slotinpod for pod bidding support
4.4 4.4.1	Substitution Macros Added AUCTION_MIN_TO_WIN
4.2.3	Object: Bid Added apis
3.2.4	Object: Imp Added rwdd
3.2.1 3.2.14 4.2.3	Object: App, Bid, BidRequest Clarified language around use of storeid vs bundle
3.2.4	Object Imp Added ssai
3.2.18	Object: Device Clarified language around mccmnc and roaming
3.2.23 3.2.24	Added Objects: Network, Channel, SupplyChain, SupplyChainNode, EIDs and UIDs
4.2.3	Object Bid Added mtype
3.2.6 3.2.7 3.2.16	Removed previously deprecated attributes Object: Banner, wmax, hmax, wmin, hmin Object: Video, protocol Object: Content, videoquality
7.6	Pod Bidding for Video and Audio implementers guide
7.7	Network and Channel object examples
3.2.7 3.2.8 3.2.18 3.2.20 4.2.3	Deprecated attributes Object: Video, sequence Object: Audio, sequence Object: Device, didsha1, didmd5, dpidsha1, dpidmd5, macsha1, macmd5 Object: User, yob, gender Object: Bid, api
7.8	Added Counting Billable events and tracked ads
3.2.29 3.2.30	Object: UserAgent & Object Brand Version added
	
Version 2.4 to 2.5:
	
	
	//insert table from page 89
	
Section	Description
2.4
Section: Data Encoding New section added.
3.1
Object Model: Bid Request Updated to include Source and Metric objects.
3.2.1
Object: BidRequest Attributes bseat, wlang, and source have been added.
3.2.2
Object: Source New Source object has been added including the Payment ID pchain attribute.
3.2.4
Object: Imp Attribute metric has been added.
3.2.5
Object: Metric New Metric object has been added.
3.2.6
Object: Banner Attribute vcm has been added.
3.2.7
Object: Video Attributes placement and playbackend have been added. Guidance added to use only the first element of attribute playbackmethod in preparation for future conversion to an integer.
3.2.10
Object: Format Attributes wratio, hratio, and wmin have been added.
3.2.13	Object: Device Attribute mccmnc has been added. Attribute carrier has been clarified to eliminate a reference to using “WIFI” as a carrier.
4.2.3
Object: Bid Attributes burl, lurl, tactic, language, wratio, and hratio have been added.
4.4
Substitution Macros: Macros ${AUCTION_MBR} and ${AUCTION_LOSS} have been added. A best practice has been added to use “AUDIT” for unknown values when rendering for test or quality purposes.
5.6
List: API Frameworks Item 6 has been added.
5.9
List: Video Placement Types New list has been added.
5.10
List: Playback Methods Items 5-6 have been added.
5.11
List: Playback Cessation Modes New list has been added.
5.24
List: No-Bid Reason Codes Items 9-10 have been added.
5.25
List: Loss Reason Codes New list has been added.

