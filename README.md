![IAB Tech Lab](https://drive.google.com/uc?id=10yoBoG5uRETSXRrnJPUDuONujvADrSG1)

# **OpenRTB 2.x**
OpenRTB 2.x specification, from 2.6 onward

#### About OpenRTB
https://iabtechlab.com/openrtb  


#### AdCOM: Advertising Common Object Model
https://github.com/InteractiveAdvertisingBureau/AdCOM

#### Versioning Policy
As of OpenRTB 2.6-202211, OpenRTB's version number is only incremented on breaking changes. In other words, OpenRTB 2.7 should be considered a distinct version from OpenRTB 2.6 when there is a need for distinguishing versions. For example, a demand source might regard the version header when parsing a bid request received from a supply source. See OpenRTB Principles.

The current version of the OpenRTB specification is updated approximately once a month if there are non-breaking improvements to be released such as new fields, objects, or values in enumerated lists. Errata, such as clarifications or corrections to descriptions not materially impacting the specification itself, are also addressed during monthly updates. See Errata.

The format for version numbering includes major and minor version and a date code. For example, 2.6-202211 represents the release for November 2022. The following releases may be 2.6-202212 (December), 2.6-202301 (January), etc.

This versioning policy is a break from historical practice for OpenRTB 2.x. In versions of OpenRTB prior to 2.6, major version numbers represent breaking changes and minor version numbers represent non-breaking changes.

#### How To Contribute

1. Create a fork of this GitHub repo in your own GitHub account
1. Create a new branch in your fork, based on `develop`, giving your new branch a short but descriptive name (e.g. if you're adding support for a new flux capacitor object, you could call the branch "add-flux-capacitor")
1. Make the desired changes in your branch, with one commit per logical change (e.g. if you're adding 2 distinct features in your branch, create 2 distinct commits). Give each of your commits a short but descriptive "Summary" name, and then provide a longer "Description" to fully explain your proposed changes.
1. (Optional) Consider doing a round of internal reviews/feedback within your own organization, and make any additional updates in your own branch.
1. Once you're happy with your branch, publish it to GitHub. Then create a new Pull Request (PR) to propose merging the changes from your fork into the `develop` branch of the origin repo.
1. The Programmatic Supply Chain Working Group and Commit Group will review your update(s), leave comments, and may propose changes. You may need to make additional commits to receive approval for your PR.
1. Once your PR is approved, it will be merged into the `main` branch at the time of the next monthly release. Details below on how the Release Process works.
1. (Optional) If your PR has been open for a long time, it's possible that it cannot be automatically merged into the `develop` branch. In this case, there will be a message in the PR asking you to resolve conflicts before it can be merged.

#### Monthly Release-Cutting Process (for repo admins)

Over the course of each month, the Programmatic Supply Chain Working Group and Commit Group may review any submitted PRs and take the following possible actions for each:
- approve it for inclusion in the next release
- ask the author(s) for additional changes
- reject it (with a rationale)

During the last week of the month, if there are any approved PRs in the `develop` branch, the following steps are executed:

1. A PR is created to merge the `develop` branch into the `main` branch.
1. A new Release and Tag are created concurrently. The naming convention for the release is "OpenRTB v2.6-YYYYMM", and the tag is "2.6-YYYYMM" where YYYYMM is the date code (e.g. 202301 for January 2023).

The result of this process is that tagged releases are created for each release of OpenRTB, and the history of these is easily reviewed. The `main` branch for the repository will always reflect the most recent release, and ongoing development work will always occur in the `develop` branch.

#### Contact
For more information, or to get involved, please email support@iabtechlab.com.

#### About IAB Tech Lab  
The IAB Technology Laboratory is a nonprofit research and development consortium charged
with producing and helping companies implement global industry technical standards and
solutions. The goal of the Tech Lab is to reduce friction associated with the digital advertising and marketing supply chain while contributing to the safe growth of an industry. The IAB Tech Lab spearheads the development of technical standards, creates and maintains a code library to assist in rapid, cost-effective implementation of IAB standards, and establishes a test platform for companies to evaluate the compatibility of their technology solutions with IAB standards, which for 18 years have been the foundation for interoperability and profitable growth in the digital advertising supply chain.

Learn more about IAB Tech Lab here: [https://www.iabtechlab.com/](https://www.iabtechlab.com/)


#### Contributors and Technical Governance

OpenRTB Working Group members provide contributions to this repository. Participants in the Programmatic Supply Working group must be members of IAB Tech Lab. Technical Governance and code commits for the project are provided by the IAB Tech Lab Programmatic Supply Chain Commit Group. 

Learn more about how to submit changes in our working group: [So, You'd Like to Propose a Change...](http://iabtechlab.com/blog/so-youd-like-to-propose-a-change-to-openrtb-adcom/)

### License
OpenRTB Specification the IAB Tech Lab is licensed under a Creative Commons Attribution 3.0 License.   To view a copy of this license, visit creativecommons.org/licenses/by/3.0/ or write to Creative Commons, 171 Second Street, Suite 300, San Francisco, CA 94105, USA.

By submitting an idea, specification, software code, document, file, or other material (each, a “Submission”) to the OpenRTB repository, to any member of the Programmatic Supply Chain Working Group, or to the IAB Tech Lab in relation to OpenRTB 2.x you agree to and hereby license such Submission to the IAB Tech Lab under the Creative Commons Attribution 3.0 License and agree that such Submission may be used and made available to the public under the terms of such license. If you are a member of the IAB Tech Lab then the terms and conditions of the [IPR Policy](https://iabtechlab.com/ipr-iab-techlab/acknowledge-ipr/) may also be applicable to your Submission, and if the IPR Policy is applicable to your Submission then the IPR Policy will control  in the event of a conflict between the Creative Commons Attribution 3.0 License and the IPR Policy.

#### Disclaimer

THE STANDARDS, THE SPECIFICATIONS, THE MEASUREMENT GUIDELINES, AND ANY OTHER MATERIALS OR SERVICES PROVIDED TO OR USED BY YOU HEREUNDER (THE “PRODUCTS AND SERVICES”) ARE PROVIDED “AS IS” AND “AS AVAILABLE,” AND IAB TECHNOLOGY LABORATORY, INC. (“TECH LAB”) MAKES NO WARRANTY WITH RESPECT TO THE SAME AND HEREBY DISCLAIMS ANY AND ALL EXPRESS, IMPLIED, OR STATUTORY WARRANTIES, INCLUDING, WITHOUT LIMITATION, ANY WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AVAILABILITY, ERROR-FREE OR UNINTERRUPTED OPERATION, AND ANY WARRANTIES ARISING FROM A COURSE OF DEALING, COURSE OF PERFORMANCE, OR USAGE OF TRADE. TO THE EXTENT THAT TECH LAB MAY NOT AS A MATTER OF APPLICABLE LAW DISCLAIM ANY IMPLIED WARRANTY, THE SCOPE AND DURATION OF SUCH WARRANTY WILL BE THE MINIMUM PERMITTED UNDER SUCH LAW. THE PRODUCTS AND SERVICES DO NOT CONSTITUTE BUSINESS OR LEGAL ADVICE. TECH LAB DOES NOT WARRANT THAT THE PRODUCTS AND SERVICES PROVIDED TO OR USED BY YOU HEREUNDER SHALL CAUSE YOU AND/OR YOUR PRODUCTS OR SERVICES TO BE IN COMPLIANCE WITH ANY APPLICABLE LAWS, REGULATIONS, OR SELF-REGULATORY FRAMEWORKS, AND YOU ARE SOLELY RESPONSIBLE FOR COMPLIANCE WITH THE SAME, INCLUDING, BUT NOT LIMITED TO, DATA PROTECTION LAWS, SUCH AS THE PERSONAL INFORMATION PROTECTION AND ELECTRONIC DOCUMENTS ACT (CANADA), THE DATA PROTECTION DIRECTIVE (EU), THE E-PRIVACY DIRECTIVE (EU), THE GENERAL DATA PROTECTION REGULATION (EU), AND THE E-PRIVACY REGULATION (EU) AS AND WHEN THEY BECOME EFFECTIVE.
