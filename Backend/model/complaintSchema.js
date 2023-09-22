const mongoose = require("mongoose");

const complaintSchema = new mongoose.Schema({
    employeeId: {
        type: String,
        // required: true
    },
    userId: {
        type: String,
        // required: true
    },
    username:{
        type:String
    },
    userLocation:{
        type:String
    },
    complaint :{
        type: String,
        // required: true
    },
    bank:{
        type: String,
        // required: true
    },
    status:{
        type: String,
        // required: true
    },
    type:{
        type: String,
        // required: true
    },
    documents:{
        type: [
            {
                documentName: {
                    type: String,
                    // required: true
                },
                documentUrl: {
                    type: String,
                    // required: true
                }
            }
        ]
        // required: true
    },
});

const Complaint = new mongoose.model("Complaint", complaintSchema);

module.exports = Complaint;