//
//  Employee.swift
//  MaddenJonathan-hw8
//
//  Created by John Madden on 4/5/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import Foundation

// This class is used to hold the data displayed in the Show Employee View Controller
class Employee {
    var firstName:String
    var lastName:String
    var department:String
    var jobTitle:String
    
    // Initializing the employee object
    init(firstName:String, lastName:String, department:String, jobTitle:String) {
        self.firstName = firstName
        self.lastName = lastName
        self.department = department
        self.jobTitle = jobTitle
    }
}
