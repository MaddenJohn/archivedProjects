//
//  Automobile.swift
//  maddenjohn-hw1
//
//  Created by Jonathan Madden on 1/27/17.
//  Copyright © 2017 cs378. All rights reserved.
//
//  This class creates an automobile with 4 properties
//  make, model, number of doors, and speed generic
//  methods to get and set are implemented for all
//  but the speed property and an increase and decrease
//  method is also implemented for the speed property

import Foundation

class Automobile {
    private var _make:String
    private var _model:String
    private var _numberOfDoors:Int
    private var _speed:Int
    
    init(make:String, model:String, numberOfDoors:Int, speed:Int) {
        _make = make
        _model = model
        _numberOfDoors = numberOfDoors
        _speed = speed
    }
    
    // utilizes init to create an Automobile easily
    class func create(make:String, model:String, numberOfDoors:Int, speed:Int) -> Automobile {
        return Automobile(make: make,model: model,numberOfDoors: numberOfDoors,speed: speed)
    }
    
    func getMake() -> String {
        return _make
    }
    
    func getModel() -> String {
        return _model
    }
    
    func getNumberOfDoors() -> Int {
        return _numberOfDoors
    }
    
    func getSpeed() -> Int {
        return _speed
    }
    
    func setMake(make:String){
        _make = make
    }
    
    func setModel(model:String){
        _model = model
    }
    
    func setNumberOfDoors(numberOfDoors:Int){
        _numberOfDoors = numberOfDoors
    }
    
    // increase speed and check for return values within 0 - 150
    func increaseSpeed(speedChange:Int){
        _speed += speedChange
        if(_speed > 150){
            _speed = 150
        }
        else if(_speed < 0) {
            _speed = 0
        }
    }
    
    // decrease speed and check for return values within 0 - 150
    func decreaseSpeed(speedChange:Int){
        _speed -= speedChange
        if(_speed > 150){
            _speed = 150
        }
        else if(_speed < 0) {
            _speed = 0
        }
    }
    
    // return String value for easy printing
    func description() -> String{
        return "Make: \(_make), Model: \(_model), NumDoors: \(_numberOfDoors), Speed: \(_speed)"
    }
    
}
