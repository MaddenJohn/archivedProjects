//
//  AddressTableViewCell.swift
//  MaddenJonathan-hw4
//
//  Created by John Madden on 2/18/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import UIKit

// CustomTableViewCell to display the address information
class AddressTableViewCell: UITableViewCell {
    @IBOutlet weak var streetLabel: UILabel!
    @IBOutlet weak var cityLabel: UILabel!
    @IBOutlet weak var stateLabel: UILabel!
    @IBOutlet weak var zipLabel: UILabel!

    override func awakeFromNib() {
        super.awakeFromNib()
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)
    }
}
