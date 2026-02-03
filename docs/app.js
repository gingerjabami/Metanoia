const topicSequence = [
  ["Arrays", ["Two pointers", "Sliding window", "Prefix sums"]],
  ["Hashing", ["Frequency maps", "Set membership"]],
  ["Stacks", ["Monotonic stack", "Bracket matching"]],
  ["Binary Search", ["Lower/upper bound", "Binary search on answer"]],
  ["Trees", ["DFS", "BFS", "Binary lifting"]],
  ["Graphs", ["BFS", "DFS", "Dijkstra"]],
  ["DP", ["1D DP", "2D DP", "Knapsack"]],
];

const xpPerTask = {
  easy: 50,
  medium: 120,
  hard: 240,
  review: 40,
  concept: 60,
  contest: 300,
};

const form = document.getElementById("plan-form");
const mainContainer = document.getElementById("main-quests");
const sideContainer = document.getElementById("side-quests");
const bonusContainer = document.getElementById("bonus-quests");
const jsonOutput = document.getElementById("json-output");

const statStreak = document.getElementById("stat-streak");
const statWeekly = document.getElementById("stat-weekly");
const statXp = document.getElementById("stat-xp");

function difficultyTag(level) {
  if (level <= 2) return "easy";
  if (level <= 5) return "normal";
  return "hard";
}

function buildQuests(topic, subtopics, tag) {
  if (tag === "easy") {
    return {
      main: [
        buildQuest(`Solve 2 Easy problems: ${topic}`, topic, "easy", 2, 50),
        buildQuest(`Solve 1 Medium problem: ${subtopics[0]}`, subtopics[0], "medium", 1, 120),
      ],
      bonus: [],
    };
  }
  if (tag === "normal") {
    return {
      main: [
        buildQuest(`Solve 2 Medium problems: ${topic}`, topic, "medium", 2, 120),
        buildQuest(`Solve 1 Medium problem: ${subtopics[1]}`, subtopics[1], "medium", 1, 120),
      ],
      bonus: [],
    };
  }
  return {
    main: [
      buildQuest(`Solve 2 Medium problems: ${topic}`, topic, "medium", 2, 120),
      buildQuest(`Solve 1 Hard problem: ${subtopics[2]}`, subtopics[2], "hard", 1, 240),
    ],
    bonus: [
      buildQuest(`Time-boxed Hard sprint: 1 problem (${topic})`, topic, "hard", 1, 240),
    ],
  };
}

function buildQuest(title, topic, difficulty, count, xp) {
  return { title, topic, difficulty, count, xp };
}

function buildSideQuests(topic) {
  return [
    buildQuest(`Review one editorial: ${topic} patterns`, topic, "concept", 1, 60),
    buildQuest("Re-solve 1 previously missed problem", "Revision", "review", 1, 40),
  ];
}

function renderQuestList(container, quests) {
  container.innerHTML = "";
  if (!quests.length) {
    container.innerHTML = "<p class=\"empty\">No bonus quests today.</p>";
    return;
  }
  quests.forEach((quest) => {
    const card = document.createElement("div");
    card.className = "quest-card";
    card.innerHTML = `
      <div class="quest-title">${quest.title}</div>
      <div class="quest-meta">
        <span>${quest.topic}</span>
        <span>${quest.count}x • ${quest.difficulty.toUpperCase()} • ${quest.xp} XP</span>
      </div>
    `;
    container.appendChild(card);
  });
}

function updateStats(plan) {
  statStreak.textContent = plan.streak_status.daily_streak;
  statWeekly.textContent = plan.streak_status.weekly_streak;
  statXp.textContent = plan.total_xp_available;
}

function generatePlan() {
  const level = Number(document.getElementById("level").value || 1);
  const streak = Number(document.getElementById("streak").value || 0);
  const weekly = Number(document.getElementById("weekly").value || 0);
  const date = document.getElementById("plan-date").value || new Date().toISOString().slice(0, 10);

  const tag = difficultyTag(level);
  const [topic, subtopics] = topicSequence[level % topicSequence.length];
  const { main, bonus } = buildQuests(topic, subtopics, tag);
  const side = buildSideQuests(topic);

  const totalXp = [...main, ...side, ...bonus].reduce(
    (sum, quest) => sum + quest.xp * quest.count,
    0,
  );

  const plan = {
    date,
    main_quests: main,
    side_quests: side,
    bonus_quests: bonus,
    xp_per_task: xpPerTask,
    total_xp_available: totalXp,
    streak_status: {
      daily_streak: streak,
      weekly_streak: weekly,
    },
    difficulty_tag: tag,
  };

  renderQuestList(mainContainer, main);
  renderQuestList(sideContainer, side);
  renderQuestList(bonusContainer, bonus);
  updateStats(plan);
  jsonOutput.textContent = JSON.stringify(plan, null, 2);
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  generatePlan();
});

const dateInput = document.getElementById("plan-date");
if (!dateInput.value) {
  dateInput.value = new Date().toISOString().slice(0, 10);
}

generatePlan();
