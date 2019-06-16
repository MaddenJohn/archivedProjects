//
//  ShowEmployeeTableViewCell.swift
//  MaddenJonathan-hw8
//
//  Created by John Madden on 4/5/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import UIKit

// Custom cell class for holding protocals
class ShowEmployeeTableViewCell: UITableViewCell {
    @IBOutlet weak var fName: UILabel!
    @IBOutlet weak var lName: UILabel!
    @IBOutlet weak var dept: UILabel!
    @IBOutlet weak var title: UILabel!

    override func awakeFromNib() {
        super.awakeFromNib()
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)
    }
}
