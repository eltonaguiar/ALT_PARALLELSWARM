# Discovery Guided Setup

- Source: https://www.servicenow.com/docs/r/zurich/it-operations-management/discovery/discovery-guided-setup.html
- Release: Zurich
- Map: itom

---

# Discovery Guided Setup

Summarize Summarized using AI This content was generated using new OpenAI-powered functionality. Results are provided on an as is basis and are not guaranteed to be accurate or complete. Summary of Discovery Guided Setup ITOM Discovery Guided Setup offers a structured sequence of tasks designed to help you install and configure Discovery efficiently in your ServiceNow environment. It is especially beneficial for first-time setups, enabling quick deployment and foundational configuration for accurate visibility in the Configuration Management Database (CMDB) and effective IT operations. Show full answer Show less Note that this guided setup has been superseded by the ITOM Configuration Console (available from Zurich Patch 8 onwards), which provides a faster, more interactive approach to installation and configuration, including task assignment and automated implementation via ServiceNow Otto. The current guided setup includes a task linking directly to the ITOM Configuration Console for seamless transition. You can access the guided setup by navigating to All > ITOM Guided Setup > ITOM Discovery Guided Setup . It allows saving and resuming progress by naming your configuration, with easy access to ongoing configurations. Phases The setup is divided into four progressive phases, each with embedded help and documentation links to assist you throughout: Learn: Introduces core Discovery principles, techniques, and prerequisites. Crawl: Guides you through technical setup, including plugin installation, credential configuration, and instance preparation for scheduled discoveries. Walk: Focuses on configuring and activating Discovery schedules, adding credentials, and installing/validating MID Servers. Run: Emphasizes monitoring and optimizing Discovery using tools like Discovery Admin Workspace and Content 360. Key Features The guided setup provides intuitive navigation and progress tracking with interactive features both on the landing page and within each phase, enabling you to manage tasks efficiently: Landing page features: Exit setup, mark setup complete (after all tasks are done), start phases, track progress, jump to specific tasks, and switch between phases. In-phase features: Return to landing page, toggle phases, navigate between activities, mark tasks complete to proceed, and skip activities as needed. This setup structure facilitates a smooth, step-by-step configuration experience, ensuring you can deploy and optimize Discovery effectively while maintaining visibility into your progress.
ITOM
Discovery
Guided Setup
provides a sequence of tasks that help you install and get started with
Discovery
. If you're setting up
Discovery
for the first time, this is a good way to get your environment up and running quickly.

Note:
This guided setup has been replaced by the
ITOM
Configuration Console (available in Zurich Patch 8 or later versions of the
ServiceNow AI Platform
), which offers a faster way to install and update apps, with interactive configuration pages, task assignment, and automated implementation by
ServiceNow Otto
. In
ITOM
Guided Setup v27.3.1, the Learn phase includes a new task that provides direct access to the
ITOM
Configuration Console. For more information, see
ITOM Configuration Console for Discovery
.
To access the
ITOM
Discovery
Guided Setup
, navigate to
All > ITOM Guided Setup > ITOM Discovery Guided Setup
. You're then prompted to enter a configuration name, which enables your progress to be saved and resumed later. If you're returning to the setup, select
Cancel
followed by
Exit
in the confirmation dialog to view the list of in-progress setup configurations.
The
ITOM
Discovery
Guided Setup
leads you through a structured series of configuration activities to promote accurate visibility in the
Configuration Management Database (CMDB)
and establish a strong foundation for IT operations.

## Phases

The setup is organized into the four distinct phases: Learn, Crawl, Walk, and Run. Each task within a phase includes built-in resources, such as contextual embedded help and links to detailed documentation on the
ServiceNow
product documentation site. In some cases, you can even complete the task directly within the guided setup.

Learn
The Learn phase is the first step in the guided setup. It covers core principles, techniques, and prerequisites for
Discovery
.
Crawl
This phase walks you through the initial technical setup of
Discovery
, including installing the necessary plug-ins, configuring credentials, and preparing your instance for scheduling discoveries.
Walk
In this phase, you configure and activate
Discovery
schedules by setting up various schedule types, adding credentials, and installing and validating your
MID Servers
.
Run
This phase focuses on monitoring and optimizing ongoing
Discovery
operations, leveraging tools like
Discovery Admin Workspace
and Content 360 to track performance and promote continued success.

## Key features

The
ITOM
Discovery
Guided Setup
provides step-by-step configuration support along with intuitive navigation to track progress and move smoothly through each phase.
Figure 1. Guided Setup landing page features
Table 1. Interactive features within the landing page
Feature Description
1. Exit Exit the Guided Setup . Note: Selecting Exit in the confirmation dialog takes you back to the list of setup configurations currently in progress. 2. Complete Mark the Guided Setup complete. Note: This option is only available once you have completed all the tasks in each phase of the setup. 3. Start Launch the Guided Setup phase. 4. Status Track your progress of the Guided Setup phase. 5. Task Jump to specific activities within a phase. 6. Phase drop-down View and access tasks within another phase.
Figure 2. Guided Setup in-phase features
Table 2. Interactive features within each phase
Feature Description
1. Back arrow Return to the Guided Setup landing page. 2. Phase drop-down Toggle between different phases. 3. Activities Jump to other activities within the current phase. 4. Close Navigate back to the Guided Setup landing page. 5. Mark Complete Track your progress and continue to the next activity in the phase. 6. Skip Skip directly to the next activity in the phase.
