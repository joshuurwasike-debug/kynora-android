
const pageContent = document.getElementById("pageContent");
const pageTitle = document.getElementById("pageTitle");
const sidebar = document.getElementById("sidebar");
// API CONNECTION
const API_BASE_URL = "http://127.0.0.1:8000";

function apiUrl(path) {
  return `${API_BASE_URL}${path}`;
}
const pageInfo = {
  dashboard: {
    title: "Dashboard",
    description: "Your business operations overview.",
    icon: "⌂"
  },
  contacts: {
    title: "Contacts",
    description: "Manage your customers and business relationships.",
    icon: "♙"
  },
  leads: {
    title: "Leads",
    description: "Track potential customers and opportunities.",
    icon: "◎"
  },
  inbox: {
    title: "Inbox",
    description: "Keep track of your business conversations.",
    icon: "✉"
  },
  tasks: {
    title: "Tasks",
    description: "Organise work and stay on top of deadlines.",
    icon: "✓"
  },
  calendar: {
    title: "Calendar",
    description: "Organise your business schedule.",
    icon: "▦"
  },
  campaigns: {
    title: "Campaigns",
    description: "Plan and manage marketing activities.",
    icon: "↗"
  },
  workflows: {
    title: "Workflows",
    description: "Build automated business processes.",
    icon: "⟳"
  },
  analytics: {
    title: "Analytics",
    description: "Understand your business performance.",
    icon: "▥"
  },
  assistant: {
    title: "AI Assistant",
    description: "Your intelligent business assistant.",
    icon: "✧"
  },
  knowledge: {
    title: "Knowledge Base",
    description: "Keep important business information organised.",
    icon: "▤"
  },
  settings: {
    title: "Settings",
    description: "Customise your KYNORA workspace.",
    icon: "⚙"
  }
};

function navigateTo(page) {
  if (!pageInfo[page]) return;

  document.querySelectorAll(".nav-item").forEach(button => {
    button.classList.toggle(
      "active",
      button.dataset.page === page
    );
  });

  pageTitle.textContent = pageInfo[page].title;
  sidebar.classList.remove("open");

  if (page === "dashboard") {
    renderDashboard();
    return;
  }

  pageContent.innerHTML = `
    <div class="welcome-row">
      <div>
        <span class="eyebrow">KYNORA WORKSPACE</span>
        <h1>${pageInfo[page].icon} ${pageInfo[page].title}</h1>
        <p>${pageInfo[page].description}</p>
      </div>
    </div>

    <article class="panel page-placeholder">
      <div class="placeholder-icon">${pageInfo[page].icon}</div>
      <h2>${pageInfo[page].title}</h2>
      <p>
        This workspace is being prepared.
        Its interactive features will be added as we build
        each module.
      </p>
      <button class="primary-button" onclick="navigateTo('dashboard')">
        Return to dashboard
      </button>
    </article>
  `;
}

function renderDashboard() {
  pageContent.innerHTML = `
    <div class="welcome-row">
      <div>
        <span class="eyebrow">BUSINESS OVERVIEW</span>
        <h1>Welcome to KYNORA</h1>
        <p>Your business operations, all in one place.</p>
      </div>
      <button class="primary-button" id="quickAction">
        ＋ Quick action
      </button>
    </div>

    <div class="stats-grid">
      <article class="stat-card">
        <span>Total contacts</span>
        <strong id="contactCount">—</strong>
        <small>People in your workspace</small>
      </article>
      <article class="stat-card">
        <span>Active leads</span>
        <strong>0</strong>
        <small>Potential customers</small>
      </article>
      <article class="stat-card">
        <span>Pending tasks</span>
        <strong>0</strong>
        <small>Tasks to complete</small>
      </article>
      <article class="stat-card">
        <span>Workflows</span>
        <strong>0</strong>
        <small>Automations created</small>
      </article>
    </div>

    <div class="dashboard-grid">
      <article class="panel">
        <div class="panel-heading">
          <div>
            <h3>Business activity</h3>
            <p>Your workspace at a glance</p>
          </div>
          <span class="live-label">LIVE OVERVIEW</span>
        </div>
        <div class="chart-placeholder">
          <div class="chart-bars">
            <i style="height:35%"></i>
            <i style="height:55%"></i>
            <i style="height:42%"></i>
            <i style="height:75%"></i>
            <i style="height:60%"></i>
            <i style="height:90%"></i>
            <i style="height:68%"></i>
          </div>
          <div class="chart-days">
            <span>Mon</span><span>Tue</span><span>Wed</span>
            <span>Thu</span><span>Fri</span><span>Sat</span><span>Sun</span>
          </div>
        </div>
      </article>

      <article class="panel">
        <div class="panel-heading">
          <div>
            <h3>Quick access</h3>
            <p>Manage your operations</p>
          </div>
        </div>
        <div class="quick-links">
          <button data-page="contacts">＋ Add contact <span>→</span></button>
          <button data-page="tasks">✓ Manage tasks <span>→</span></button>
          <button data-page="assistant">✧ Open AI assistant <span>→</span></button>
          <button data-page="analytics">▥ View analytics <span>→</span></button>
        </div>
      </article>
    </div>

    <article class="panel recent-panel">
      <div class="panel-heading">
        <div>
          <h3>Recent contacts</h3>
          <p>Your latest workspace contacts</p>
        </div>
        <button class="text-button" data-page="contacts">View all →</button>
      </div>
      <div id="recentContacts" class="empty-state">
        Your contacts will appear here.
      </div>
    </article>
  `;

  loadDashboardContacts();

  document.getElementById("quickAction").onclick = () => {
    navigateTo("contacts");
  };
}

async function loadDashboardContacts() {
  const token = localStorage.getItem("kynora_token");
  if (!token) return;

  try {
    const response = await fetch(apiUrl("/api/contacts/"), {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (!response.ok) return;

    const contacts = await response.json();

    const count = document.getElementById("contactCount");
    const recent = document.getElementById("recentContacts");

    if (count) count.textContent = contacts.length;

    if (recent) {
      recent.innerHTML = contacts.length
        ? contacts.slice(0, 5).map(contact => `
            <div class="contact-row">
              <strong>${escapeHTML(contact.name)}</strong>
              <span>${escapeHTML(contact.email || contact.company || "No additional details")}</span>
            </div>
          `).join("")
        : "No contacts added yet.";
    }
  } catch (error) {
    console.error("Could not load dashboard contacts:", error);
  }
}

function escapeHTML(value) {
  return String(value).replace(/[&<>"']/g, character => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  })[character]);
}

document.addEventListener("click", event => {
  const pageButton = event.target.closest("[data-page]");

  if (pageButton) {
    navigateTo(pageButton.dataset.page);
  }
});

document.getElementById("themeToggle").addEventListener("click", () => {
  document.body.classList.toggle("light-theme");

  localStorage.setItem(
    "kynora_theme",
    document.body.classList.contains("light-theme")
      ? "light"
      : "dark"
  );
});

document.getElementById("menuToggle").addEventListener("click", () => {
  sidebar.classList.toggle("open");
});

if (localStorage.getItem("kynora_theme") === "light") {
  document.body.classList.add("light-theme");
}

navigateTo("dashboard");

// KYNORA AUTHENTICATION

const authScreen = document.getElementById("authScreen");
const appShell = document.querySelector(".app-shell");
const registerForm = document.getElementById("registerForm");
const loginForm = document.getElementById("loginForm");
const authMessage = document.getElementById("authMessage");
const authTitle = document.getElementById("authTitle");
const authDescription = document.getElementById("authDescription");

function showAuthMode(mode) {
  const registering = mode === "register";

  registerForm.hidden = !registering;
  loginForm.hidden = registering;

  authTitle.textContent = registering
    ? "Create your account"
    : "Welcome back";

  authDescription.textContent = registering
    ? "Register to get started with KYNORA."
    : "Log in to access your business workspace.";

  authMessage.textContent = "";
  authMessage.classList.remove("error");
}

function showAuthError(message) {
  authMessage.textContent = message;
  authMessage.classList.add("error");
}

function showWorkspace() {
  authScreen.style.display = "none";
  appShell.style.display = "flex";
  navigateTo("dashboard");
  addLogoutButton();
}

function addLogoutButton() {
  if (document.getElementById("logoutButton")) return;

  const topActions = document.querySelector(".top-actions");
  const logout = document.createElement("button");

  logout.id = "logoutButton";
  logout.className = "icon-button";
  logout.textContent = "↪";
  logout.title = "Log out";

  logout.addEventListener("click", () => {
    localStorage.removeItem("kynora_token");
    document.getElementById("logoutButton")?.remove();

    appShell.style.display = "none";
    authScreen.style.display = "grid";

    loginForm.reset();
    registerForm.reset();
    showAuthMode("register");
  });

  topActions.appendChild(logout);
}

document.getElementById("showLogin").addEventListener("click", () => {
  showAuthMode("login");
});

document.getElementById("showRegister").addEventListener("click", () => {
  showAuthMode("register");
});

// REGISTER ACCOUNT

registerForm.addEventListener("submit", async event => {
  event.preventDefault();

  const submitButton = registerForm.querySelector(
    'button[type="submit"]'
  );

  submitButton.disabled = true;
  submitButton.textContent = "Creating account...";

  const formData = new FormData(registerForm);

  const data = {
    full_name: formData.get("full_name").trim(),
    email: formData.get("email").trim(),
    password: formData.get("password"),
    workspace_name: formData.get("workspace_name").trim(),
    business_type: formData.get("business_type").trim() || null
  };

  try {
    const response = await fetch(apiUrl("/api/auth/register"), {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (!response.ok) {
      const detail = Array.isArray(result.detail)
        ? result.detail.map(item => item.msg).join(", ")
        : result.detail || "Registration failed.";

      throw new Error(detail);
    }

    loginForm.elements.email.value = data.email;
    loginForm.reset();

    showAuthMode("login");
    authMessage.textContent =
      "Account created successfully! Please log in.";

  } catch (error) {
    showAuthError(error.message);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Create account →";
  }
});

// LOGIN

loginForm.addEventListener("submit", async event => {
  event.preventDefault();

  const submitButton = loginForm.querySelector(
    'button[type="submit"]'
  );

  submitButton.disabled = true;
  submitButton.textContent = "Logging in...";

  const formData = new FormData(loginForm);

  try {
    const response = await fetch(apiUrl("/api/auth/login"), {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        email: formData.get("email").trim(),
        password: formData.get("password")
      })
    });

    const result = await response.json();

    if (!response.ok) {
      const detail = Array.isArray(result.detail)
        ? result.detail.map(item => item.msg).join(", ")
        : result.detail || "Login failed.";

      throw new Error(detail);
    }

    localStorage.setItem("kynora_token", result.access_token);
    loginForm.reset();
    showWorkspace();

  } catch (error) {
    showAuthError(error.message);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Log in →";
  }
});

// CHECK EXISTING LOGIN SESSION

async function initializeAuthentication() {
  authScreen.style.display = "grid";
  appShell.style.display = "none";

  const token = localStorage.getItem("kynora_token");

  if (!token) {
    showAuthMode("register");
    return;
  }

  try {
    const response = await fetch(apiUrl("/api/auth/me"), {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error("Session expired");
    }

    showWorkspace();

  } catch (error) {
    localStorage.removeItem("kynora_token");
    showAuthMode("register");
  }
}

initializeAuthentication();
