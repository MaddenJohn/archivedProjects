//
//  MyPurchase.swift
//  Nessie-iOS-Wrapper
//
//  Created by John Madden on 6/8/17.
//  Copyright © 2017 Nessie. All rights reserved.
//

import Foundation

class MyPurchase {
    var amount:Double
    var description:String
    var date:Date

    init (amount:Double, description:String, date:Date){
        self.amount = amount
        self.description = description
        self.date = date
    }
    
    func printThis(){
        print ("\(self.amount), \(self.description), \(self.date)")
    }
}
