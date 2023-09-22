const express = require('express');
const checkAuthenticated = require('./auth').checkAuthenticated;
const mongoose = require('mongoose');

const User = require('../model/userSchema');
const Employee = require('../model/employeeSchema');
const router = express.Router();

const bank_name = require('../extraAsset/bank');
router.get('/', (req, res) => {
    res.render('employee_login',{bank_name:bank_name});
});   

router.get('/user',checkAuthenticated,(req,res)=>{
    res.send('ho gya login user');
});

router.get('/employeeDashboard',checkAuthenticated,async(req,res)=>{
    try{
        const id = req.user.id;
        const employee = await Employee.findById(id);
        res.status(200).render('employee_dashboard',{employee:employee});
        // console.log(employee);
    }catch(err){
        console.log(err);
    }
});

router.get('/employeeProfile',checkAuthenticated,async(req,res)=>{
    try{
        const id = req.user.id;
        const employee = await Employee.findById(id);
        // console.log(employee);
        res.status(200).render('employee_profile' , {employee:employee});
        // console.log(employee.id,employee.Name,employee.username,employee['Banking ID'],employee['Bank Name'],employee['Branch Name'],employee['Languages Spoken'],employee['Complaint Specialization'],employee['Phone Number']);
    }catch(err){
        console.log(err);
    }
});

router.post('/updateDetail',checkAuthenticated,async(req,res)=>{
    try{
        const id = req.user.id;
        const employee = {
            name: req.body.name,
            username: req.body.username,
            employeeId: req.body.employeeId,
            bankName: req.body.bankName,
            designation: req.body.designation,
            complaintSpecialisation: req.body.complaintSpecialisation,
            language: req.body.language,
            workplace: req.body.workplace,
            mobileNo: req.body.mobileNo,

        };
        const response = await Employee.findByIdAndUpdate(id,employee);
        // console.log(employee);
        if(response){
            console.log('updated');
            res.redirect('/employeeProfile');
        }
    }catch(err){
        console.log(err);
    }
});


module.exports = router;
