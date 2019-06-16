//
//  main.swift
//  maddenjonathan-hw1
//
//  Created by John Madden on 1/28/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import Foundation

// function to generate a random value between two boundaries
func randomValueBetween(min:UInt32, max:UInt32) -> UInt32 {
    var randomValue:UInt32 = min + arc4random_uniform(UInt32(max - min + 1))
    return randomValue
}

// simulates a race between three automobiles, randomly increasing their speeds
// and printing a winner based on the final speed
func main() {
    var carOne:Automobile
    carOne = Automobile.create(make: "Maserati", model: "GranTurismo", numberOfDoors: 2, speed: 0)
    var carTwo:Automobile
    carTwo = Automobile.create(make: "Honda", model: "Accord", numberOfDoors: 4, speed: 0)
    var carThree:Automobile
    carThree = Automobile.create(make: "Tesla", model: "S 90", numberOfDoors: 2, speed: 0)
    
    for _ in 1...10 {
        carOne.increaseSpeed(speedChange: Int(randomValueBetween(min: 0, max: 16)))
        carTwo.increaseSpeed(speedChange: Int(randomValueBetween(min: 0, max: 16)))
        carThree.increaseSpeed(speedChange: Int(randomValueBetween(min: 0, max: 16)))
    }
    
    print(carOne.description())
    print(carTwo.description())
    print(carThree.description())
    
    var winnerMake:String = ""
    var winnerModel:String = ""
    var winner:Bool
    
    // determine winner based on final speed
    if(carOne.getSpeed() > carTwo.getSpeed() && carOne.getSpeed() > carThree.getSpeed()){
        winnerMake = carOne.getMake()
        winnerModel = carOne.getModel()
        winner = true
    }
    else if (carTwo.getSpeed() > carThree.getSpeed() && carTwo.getSpeed() > carOne.getSpeed()){
        winnerMake = carTwo.getMake()
        winnerModel = carTwo.getModel()
        winner = true
    }
    else if (carThree.getSpeed() > carOne.getSpeed() && carThree.getSpeed() > carTwo.getSpeed()){
        winnerMake = carThree.getMake()
        winnerModel = carThree.getModel()
        winner = true
    }
    else {
        winner = false
    }
    
    if (winner){
        print ("\(winnerMake) \(winnerModel) won!!")
    }
    else {
        print ("There was a tie!")
    }
}

main()
