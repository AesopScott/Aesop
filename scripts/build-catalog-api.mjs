import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");
const sourcePath = path.join(root, "ai-academy", "modules", "courses-data.json");
const outputArg = process.argv[2] || path.join(root, "_site", "aesop-api", "catalog.php");
const outputPath = path.resolve(process.cwd(), outputArg);

function courseUrl(course) {
  const courseId = String(course.id || "");
  if (course.format === "v2") {
    const slug = courseId.replace(/-v2$/, "");
    return `https://aesopacademy.org/ai-academy/modules/v2/${encodeURIComponent(slug)}/m1.html`;
  }
  return `https://aesopacademy.org/ai-academy/modules/electives-hub.html?course=${encodeURIComponent(courseId)}`;
}

const source = await readFile(sourcePath, "utf8");
const data = JSON.parse(source);

if (!Array.isArray(data.courses)) {
  throw new Error("Invalid courses-data.json format: missing courses array");
}

const response = {
  catalog_hash: createHash("sha256").update(source).digest("hex"),
  generated_at: new Date().toISOString(),
  courses: data.courses.map(course => ({
    id: String(course.id || ""),
    name: course.name || "",
    desc: course.desc || "",
    url: courseUrl(course),
    live: course.live === true,
  })),
};

await mkdir(path.dirname(outputPath), { recursive: true });
await writeFile(outputPath, `${JSON.stringify(response, null, 2)}\n`, "utf8");

console.log(`Wrote ${response.courses.length} courses to ${path.relative(root, outputPath)}`);
