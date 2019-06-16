//
//  Person.swift
//  MaddenJonathan-hw3
//
//  Created by John Madden on 2/11/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import Foundation

// This class is used to hold the data displayed in the Person View Controller
class Person {
    var firstName:String
    var lastName:String
    var age:Int
    var city:String
    init(firstName:String, lastName:String, age:Int, city:String) {
        self.firstName = firstName
        self.lastName = lastName
        self.age = age
        self.city = city
    }
}
