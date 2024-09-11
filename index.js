const express = require("express");
const dotenv = require("dotenv");

const connectToDatabase = require('./src/database/mongoose.database');

dotenv.config();

const app = express();

connectToDatabase();