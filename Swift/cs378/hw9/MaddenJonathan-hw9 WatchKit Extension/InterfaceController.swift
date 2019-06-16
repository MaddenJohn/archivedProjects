//
//  InterfaceController.swift
//  MaddenJonathan-hw9 WatchKit Extension
//
//  Created by John Madden on 4/12/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import WatchKit
import Foundation


class InterfaceController: WKInterfaceController {
    var index = 1
    @IBOutlet var label: WKInterfaceLabel!
    @IBOutlet var seperator: WKInterfaceSeparator!
    
    override func awake(withContext context: Any?) {
        super.awake(withContext: context)
        label.setText("My First")
        seperator.setColor(UIColor.clear)
        
        // Configure interface objects here.
    }
    
    override func willActivate() {
        // This method is called when watch view controller is about to be visible to user
        super.willActivate()
    }
    
    override func didDeactivate() {
        // This method is called when watch view controller is no longer visible
        super.didDeactivate()
    }
    
    @IBAction func btnAction() {
        if (index == 0){
            label.setText("My First")
        }
        else if (index == 1){
            label.setText("iWatch App")
        }
        else if (index == 2){
            label.setText("YAY!")
        }
        index = (index + 1) % 3
    }
    
}
