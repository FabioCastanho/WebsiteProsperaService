const mongoose = require("mongoose")

const connectToDatabase = async () => {
    await mongoose.connect()
}