//
//  myViewController.swift
//  MaddenJonathan-hw7
//
//  Created by John Madden on 3/18/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import UIKit

class myViewController: UIViewController {
    @IBOutlet weak var myLabel: UILabel!
    var directionRight:Int!

    override func viewDidLoad() {
        super.viewDidLoad()
        directionRight = 1
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    // Function to handle the swipe right action, which move the label to the right off the screen
    @IBAction func swipeRight(_ sender: Any) {
            UIView.animate(withDuration: 0.75, delay: 0, options: UIViewAnimationOptions.curveLinear,
                           animations: { self.myLabel.frame.origin =
                            CGPoint(x:self.view.frame.width + self.myLabel.frame.width, y:self.myLabel.frame.origin.y)},
                           completion: nil)
            directionRight = 1
    }

    // Function to handle the swipe left action, which move the label to the left off the screen
    @IBAction func swipeLeft(_ sender: Any) {
            UIView.animate(withDuration: 0.75, delay: 0, options: UIViewAnimationOptions.curveLinear,
                           animations: { self.myLabel.frame.origin =
                            CGPoint(x:0 - self.myLabel.frame.width, y:self.myLabel.frame.origin.y)},
                           completion: nil)
            directionRight = -1
    }
    
    // Function to handle any kind of tap on the screen. If the new position is off the screen, 
    // changes the direction and if the position is already off the screen from a swipe, then
    // sets the position to along the edge. 
    @IBAction func tapHandler(_ sender: Any) {
        if (directionRight == 1){
            if (self.myLabel.frame.origin.x + self.myLabel.frame.width + 50 >= self.view.frame.width) {
                UIView.animate(withDuration: 0.5, delay: 0, options: UIViewAnimationOptions.curveLinear,
                               animations: { self.myLabel.frame.origin =
                                CGPoint(x:self.view.frame.width - 98, y:self.myLabel.frame.origin.y)},
                               completion: nil)
                directionRight = -1
            }
            else {
                UIView.animate(withDuration: 0.5, delay: 0, options: UIViewAnimationOptions.curveLinear,
                               animations: { self.myLabel.center = CGPoint(x:self.myLabel.center.x + 50,
                                                        y:self.myLabel.center.y)},
                               completion: nil)
            }
        }
        else {
            if (self.myLabel.frame.origin.x - 50 <= 0) {
                UIView.animate(withDuration: 0.5, delay: 0, options: UIViewAnimationOptions.curveLinear,
                               animations: { self.myLabel.frame.origin =
                                CGPoint(x:0, y:self.myLabel.frame.origin.y)},
                               completion: nil)
                directionRight = 1
            }
            else {
                UIView.animate(withDuration: 0.5, delay: 0, options: UIViewAnimationOptions.curveLinear,
                           animations: { self.myLabel.center = CGPoint(x:self.myLabel.center.x - 50,
                                                                       y:self.myLabel.center.y)},
                                        completion: nil)
            }
        }
    }
}
