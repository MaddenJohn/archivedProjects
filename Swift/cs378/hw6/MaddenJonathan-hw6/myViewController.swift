//
//  myViewController.swift
//  MaddenJonathan-hw6
//
//  Created by John Madden on 2/27/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import UIKit

class myViewController: UIViewController {
    @IBOutlet weak var imgView2: UIImageView!
    var index:Int!
    
    // This is the important part of this class, which loads in the image based on the
    // initial index which is set in the my Page View Controller class
    override func viewDidLoad() {
        super.viewDidLoad()
        self.title = "myViewController"
        self.imgView2.image = UIImage(named: "wonders\(index!).png")
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
}
