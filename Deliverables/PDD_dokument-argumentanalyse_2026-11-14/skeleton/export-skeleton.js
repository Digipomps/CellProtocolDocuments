// node export-skeleton.js > analyserom-skeleton.v2.json — kompakt JSON som Swift-fabrikken bygger inn.
const { analyseromSkeleton } = require("./analyserom-skeleton.v2.js");
process.stdout.write(JSON.stringify(analyseromSkeleton));
