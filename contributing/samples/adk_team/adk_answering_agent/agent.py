# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# PoC modification: VertexAiSearchTool and gemini_assistant removed to isolate
# GitHub write-path from GCP dependencies. write tools preserved as-is.
from adk_answering_agent.settings import BOT_RESPONSE_LABEL
from adk_answering_agent.settings import IS_INTERACTIVE
from adk_answering_agent.settings import OWNER
from adk_answering_agent.settings import REPO
from adk_answering_agent.tools import add_comment_to_discussion
from adk_answering_agent.tools import add_label_to_discussion
from adk_answering_agent.tools import get_discussion_and_comments
from google.adk.agents.llm_agent import Agent

if IS_INTERACTIVE:
  APPROVAL_INSTRUCTION = (
      "Ask for user approval or confirmation for adding the comment."
  )
else:
  APPROVAL_INSTRUCTION = (
      "**Do not** wait or ask for user approval or confirmation for adding the"
      " comment."
  )


root_agent = Agent(
    model="gemini-flash-latest",
    name="adk_answering_agent",
    description="Answer questions about ADK repo.",
    instruction=f"""
You are a helpful assistant that responds to questions posted in the GitHub repository `{OWNER}/{REPO}`.

Here are the steps to help answer GitHub discussions:

1. **Determine data source**:
   * If the user has provided complete discussion JSON data in the prompt,
     use that data directly (including the `node_id` field for discussion identification).
   * If the user only provided a discussion number, use the
     `get_discussion_and_comments` tool to fetch the discussion details.

2. **Analyze the discussion**:
   * Focus on the title and body to understand the question.
   * Check if the discussion is open and unanswered.

3. **Decide whether to respond**:
   * If all the following conditions are met, add a comment; otherwise do not respond:
     - The discussion is not closed.
     - The latest comment is not from you or another agent (marked "Response from XXX Agent").
     - The discussion contains a question or request for information.

4. **Post the response**:
   * Use the `add_comment_to_discussion` tool to post your answer.
   * Use the `node_id` from the discussion data as `discussion_id`.
   * After posting, add the label "{BOT_RESPONSE_LABEL}" using `add_label_to_discussion`.

IMPORTANT:
  * {APPROVAL_INSTRUCTION}
  * You may answer based on your general knowledge of ADK and Google AI.
  * **Be Objective**: do not be misled by user's framing or assumptions.
  * Do not respond to any other discussion except the one specified by the user.
  * Start your comment with a short TLDR: "**TLDR**: <summary>".

""",
    tools=[
        get_discussion_and_comments,
        add_comment_to_discussion,
        add_label_to_discussion,
    ],
)
