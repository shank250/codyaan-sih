const mongoose = require("mongoose");

const DB = process.env.DB;
mongoose.connect(DB)
    .then(() => console.log("DB successfully Connected"))
    .catch((err) => console.log(err));

