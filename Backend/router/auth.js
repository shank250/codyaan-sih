const express = require("express");
const passport = require('passport');

const router = express.Router();

const User = require("../model/userSchema");
const Employee = require("../model/employeeSchema");


///////////////////////////////////////////////////////////  get route ////////////////////////////////////////////////////////////////////////////////////



/////////////////////////////////////////////////////////// user register post route ////////////////////////////////////////////////////////////////////////////////////

// router.post("/userRegister",async (req,res)=>{
//     const { name , username , password , cpassword} = req.body;
//     console.log(!name , !username , !password , !cpassword);
//     try{
//         if(!name || !username || !password || !cpassword ){
//             return res.status(422).json({error : "fill all the details"});
//         }
//         else if(password !== cpassword){
//             return res.status(422).json({json : "password and confirm password are not matching."})
//         }
//         else{
//             User.register(new User({name:name,username : username }), password,function(err,user){
//                 if(err){
//                     return res.send(err);            
//                 }
//                 res.send('login kar jake');
//             })
//         }
//     }
//     catch(err){
//         console.log(err);
//     };
// });

/////////////////////////////////////////////////////////// user register post route ////////////////////////////////////////////////////////////////////////////////////

router.post("/employeeRegister",async (req,res)=>{
    const { name , username ,employeeId ,designation,complaintSpecialisation ,language ,bankName ,workplace ,mobileNo , password , cpassword} = req.body;
    console.log(req.body)
    try{
        if(!name || !username  || !employeeId || !workplace || !mobileNo || !password || !cpassword || !designation || !complaintSpecialisation || !language || !bankName ){
            res.status(422).json({error : "fill all the details"});
        }
        else if(password !== cpassword){
            res.status(422).json({json : "password and confirm password are not matching."})
        }
        else{
            Employee.register(new Employee({name:name ,employeeId : employeeId ,workplace : workplace ,mobileNo : mobileNo,username : username,designation : designation,complaintSpecialisation:complaintSpecialisation,language:language,bankName:bankName}), password,function(err,user){
                if(err){
                    return res.send(err);            
                }
                res.send('login kar jake');
            })
        }
    }
    catch(err){
        console.log(err);
    };
});

/////////////////////////////////////////////////////////// login post route ////////////////////////////////////////////////////////////////////////////////////

// router.post("/userLogin",async(req,res)=>{
//     const {username , password}= req.body;
//     try{
//         if(!username || ! password){
//             return res.status(400).json({error : "fill all the details."});
//         }
//         const user = new User({
//             username : req.body.username,
//             password : req.body.password
//         });
//         req.login(user,function(err,user){
//             if(err){
//                 console.log(err);
//             }else{
//                 passport.authenticate("local")(req,res,function(){
//                     res.redirect('/index');
//                 });
//             };
//         });
        
//     }catch(err){
//         console.log(err);
//     }
// })

/////////////////////////////////////////////////////////// login post route ////////////////////////////////////////////////////////////////////////////////////

router.post("/employeeLogin",async(req,res)=>{
    const {username , password}= req.body;
    try{
        if(!username || ! password){
            return res.status(400).json({error : "fill all the details."});
        }
        const employee = new Employee({
            username : req.body.username,
            password : req.body.password
        });
        req.login(employee,function(err,user){
            if(err){
                console.log(err);
            }else{ 
                passport.authenticate("local")(req,res,function(){
                    res.redirect('/employeeDashboard');
                });
            };
        }); 
    }catch(err){
        console.log(err);
    }
})  

/////////////////////////////////////////////////////////// logout route ////////////////////////////////////////////////////////////////////////////////////

router.post('/logout',(req,res)=>{
    req.logOut((err)=>{
        if(err){
            return res.send(err);
        }
        res.send('ho gaya logout');
    })
    
})

const bank_name = require('../extraAsset/bank');
function checkAuthenticated(req,res,next){
    if (req.isAuthenticated()){
        return next();
    }
    res.render('employee_login',{bank_name:bank_name});
}

exports.router = router;
exports.checkAuthenticated = checkAuthenticated ;