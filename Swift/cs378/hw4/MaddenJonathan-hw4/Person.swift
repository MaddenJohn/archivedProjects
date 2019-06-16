//
//  Person.swift
//  MaddenJonathan-hw4
//
//  Created by John Madden on 2/18/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import Foundation

// This class is used to hold the data displayed in the Person View Controller
class Person {
    var firstName:String
    var lastName:String
    var age:Int
    var street:String
    var city:String
    var state:String
    var zip:Int
    
    // Initializing the person object
    init(firstName:String, lastName:String, age:Int, street:String, city:String, state:String, zip:Int) {
        self.firstName = firstName
        self.lastName = lastName
        self.age = age
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
    }
}
