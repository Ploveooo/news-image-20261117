// News-image entry (Node 22, standard library only): the finished picture is
// entry.png beside this file, and the program copies it to /output/entry.png.
// The image is drawn at build time by draw_news.py (Pillow); this program
// needs no network and no packages, it just moves the file.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
