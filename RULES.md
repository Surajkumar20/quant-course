# Rules of the Road

These rules exist because of how quant interviews work. A Jane Street or Citadel interviewer will hand you a problem you have never seen, on a whiteboard or in a bare editor, and watch you think.
Everything in this course is meant to build *that* ability. Code you didn't struggle with doesn't build it.

## 1. The AI policy

The goal is **minimal AI**. "Minimal" means the following.

| Allowed | Not allowed |
|---|---|
| Looking up an API ("numpy argsort descending") after you've tried the docs | Pasting a project spec or a stub into an LLM |
| Asking an LLM to **explain a concept** after you've done the OCW reading and are still confused | Inline autocomplete (Copilot, Cursor Tab, etc.) — **turn it off for this repo** |
| Asking for a **hint, not code**, after the 30-minute rule (below) | Asking an LLM to fix a failing test |
| Using AI to review a finished project's write-up for clarity | Generating tests, then "implementing" until they pass |

**Log every AI interaction** in your journal: what you asked, why, and what you learned. If the log for a project gets long, redo that project later without AI.

> Honest framing: in a real job you'll use AI tools all day. You can only use them well if you could have done the work without them. This course builds the "without".

## 2. The 30-minute rule

When you're stuck:

1. **Struggle for 30 focused minutes.** Re-read the spec, write down what you know, draw the data structure, and write a smaller test case.
2. Then go to the **OCW lecture or the book** listed in the project README.
3. Still stuck? Ask a human (study group, forum), or follow the AI policy above and ask for a *hint*.
4. Still stuck after a day? Skip the milestone, write down what blocked you, and come back after the next project.

## 3. Keep a journal

Copy [`templates/journal.md`](templates/journal.md) into each project folder as `JOURNAL.md`. Write in it daily: what you tried, what broke, what surprised you.
Interviewers ask "tell me about a bug you were stuck on". This is where your answers come from.

## Definition of Done

A project is **done** when **all** of these hold:

- [ ] All provided tests pass (`python tools/run_tests.py <project>` / `ctest -R <project>`).
- [ ] You added **at least three tests of your own**, including one edge case the provided tests miss.
- [ ] You completed every item under **Milestones** in the project README.
- [ ] `WRITEUP.md` exists, based on [`templates/writeup.md`](templates/writeup.md): a one-page explanation, at least one plot or benchmark table, and what you'd do next.
- [ ] You can answer every question under **"Explain it in an interview"** **out loud**, without notes, in under two minutes each. Record yourself.
- [ ] The project path is in `tools/enabled_projects.txt` and CI is green.

Stretch goals are optional, but the people who get the best offers usually did them.

## Workflow

```bash
git switch -c p04-black-scholes        # one branch per project
# ... work, commit often, small commits with real messages ...
python tools/run_tests.py 02-derivatives-pricing/p04-black-scholes
echo "02-derivatives-pricing/p04-black-scholes" >> tools/enabled_projects.txt
git switch main && git merge --no-ff p04-black-scholes
git push
```

Then tick the box in [`PROGRESS.md`](PROGRESS.md).

## Study groups

The course works much better with 2–4 people. Suggested rhythm:
- **Mon:** agree on the week's OCW lectures.
- **Wed:** 45-min mock interview. One person asks a puzzle from `resources/interview-prep.md` and the others solve it out loud.
- **Fri:** code review of each other's project branches. Review the code and don't rewrite it.
