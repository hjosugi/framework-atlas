const frameworks = [
  { id: "spring", number: "01", name: "Spring Boot", version: "4.1.0", kind: "Application platform", summary: "起動・自動構成・統合・運用までを標準化。", chips: ["Java 17+", "DI", "Actuator"] },
  { id: "fastapi", number: "02", name: "FastAPI", version: "0.141.1", kind: "Typed API framework", summary: "type hintをvalidation・DI・OpenAPIへ再利用。", chips: ["Python 3.10+", "ASGI", "Pydantic"] },
  { id: "gin", number: "03", name: "Gin", version: "1.12.0", kind: "HTTP framework", summary: "net/http上の薄いrouter・middleware・binding。", chips: ["Go 1.25+", "Radix", "Explicit"] },
];

const comparisons = [
  ["責任範囲", "application全体", "typed HTTP API", "HTTP request handling"],
  ["DI", "Bean container", "callable graph", "手動/外部library"],
  ["Validation", "Bean Validation", "Pydantic", "struct binding"],
  ["Concurrency", "thread / reactive", "ASGI async + workers", "goroutine"],
  ["Data", "Spring Data portfolio", "外部ORM/driver", "database/sql等"],
  ["Operations", "Actuator / Micrometer", "ASGI stackを構成", "stdlib/middlewareを構成"],
  ["主なcost", "暗黙性・startup", "blocking境界・topology", "標準形を自分で決める"],
];

const flows = [
  ["Spring Boot", ["Server", "Filter chain", "Dispatcher", "Argument resolver", "Controller", "Bean / transaction"]],
  ["FastAPI", ["ASGI server", "Middleware", "APIRoute", "Dependency graph", "Pydantic", "Endpoint / cleanup"]],
  ["Gin", ["net/http", "Engine", "Radix tree", "Pooled Context", "Middleware chain", "Handler"]],
];

const nodes = [
  { id: "spring", label: "Spring Boot", x: 200, y: 285, primary: true },
  { id: "fastapi", label: "FastAPI", x: 500, y: 285, primary: true },
  { id: "gin", label: "Gin", x: 800, y: 285, primary: true },
  { id: "spring-framework", label: "Spring Framework", x: 90, y: 100 },
  { id: "servlet", label: "Servlet", x: 260, y: 70 },
  { id: "starlette", label: "Starlette", x: 410, y: 90 },
  { id: "pydantic", label: "Pydantic", x: 590, y: 80 },
  { id: "drf", label: "DRF / Flask", x: 490, y: 490 },
  { id: "nethttp", label: "net/http", x: 730, y: 80 },
  { id: "httprouter", label: "httprouter", x: 900, y: 105 },
  { id: "nest", label: "NestJS", x: 170, y: 500 },
  { id: "echo", label: "Echo / Fiber", x: 825, y: 495 },
];
const edges = [
  ["spring-framework", "spring", "direct"], ["servlet", "spring", "direct"],
  ["starlette", "fastapi", "direct"], ["pydantic", "fastapi", "direct"], ["drf", "fastapi", "official"],
  ["nethttp", "gin", "direct"], ["httprouter", "gin", "direct"],
  ["spring", "nest", "inferred"], ["gin", "echo", "inferred"],
];

const cards = document.querySelector("#framework-cards");
cards.innerHTML = frameworks.map((f) => `<article class="card" data-id="${f.id}"><span class="number">${f.number} · ${f.kind}</span><h3>${f.name}</h3><span class="version">${f.version}</span><p>${f.summary}</p><div class="chips">${f.chips.map((chip) => `<span>${chip}</span>`).join("")}</div></article>`).join("");
document.querySelector("#comparison-body").innerHTML = comparisons.map((row) => `<tr>${row.map((cell) => `<td>${cell}</td>`).join("")}</tr>`).join("");
document.querySelector("#flows").innerHTML = flows.map(([name, steps]) => `<article class="flow"><h3>${name}</h3><ol>${steps.map((step) => `<li>${step}</li>`).join("")}</ol></article>`).join("");

document.querySelectorAll(".filter").forEach((button) => button.addEventListener("click", () => {
  document.querySelectorAll(".filter").forEach((item) => item.classList.remove("active"));
  button.classList.add("active");
  const target = button.dataset.framework;
  document.querySelectorAll(".card").forEach((card) => card.classList.toggle("hidden", target !== "all" && card.dataset.id !== target));
}));

const svg = document.querySelector("#influence-graph");
const namespace = "http://www.w3.org/2000/svg";
const byId = Object.fromEntries(nodes.map((node) => [node.id, node]));
edges.forEach(([from, to, type]) => {
  const a = byId[from], b = byId[to];
  const path = document.createElementNS(namespace, "path");
  const midY = (a.y + b.y) / 2;
  path.setAttribute("d", `M ${a.x} ${a.y} C ${a.x} ${midY}, ${b.x} ${midY}, ${b.x} ${b.y}`);
  path.setAttribute("class", `graph-edge ${type}`);
  svg.appendChild(path);
});
nodes.forEach((node) => {
  const group = document.createElementNS(namespace, "g");
  group.setAttribute("class", `graph-node${node.primary ? " primary" : ""}`);
  const circle = document.createElementNS(namespace, "circle");
  circle.setAttribute("cx", node.x); circle.setAttribute("cy", node.y); circle.setAttribute("r", node.primary ? 60 : 48);
  const label = document.createElementNS(namespace, "text");
  label.setAttribute("x", node.x); label.setAttribute("y", node.y + 4); label.textContent = node.label;
  group.append(circle, label); svg.appendChild(group);
});
