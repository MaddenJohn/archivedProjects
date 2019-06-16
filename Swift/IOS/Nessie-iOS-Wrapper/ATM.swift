//
//  ATM.swift
//  Nessie-iOS-Wrapper
//
//  Created by Lopez Vargas, Victor R. on 10/5/15.
//  Copyright (c) 2015 Nessie. All rights reserved.
//

import Foundation
import CoreLocation
import SwiftyJSON

open class ATMRequest {
    fileprivate var requestType: HTTPType?
    fileprivate var atmId: String?
    fileprivate var radius: String?
    fileprivate var latitude: Float?
    fileprivate var longitude: Float?
    fileprivate var nextPage: String?
    fileprivate var previousPage: String?
    
    public init () {
        self.requestType = HTTPType.GET
    }
    
    fileprivate func buildRequestUrl() -> String {
        if let nextPage = self.nextPage {
            return "\(baseString)\(nextPage)"
        }

        if let previousPage = self.previousPage {
            return "\(baseString)\(previousPage)"
        }
        
        var requestString = "\(baseString)/atms"

        if let atmId = self.atmId {
            requestString += "/\(atmId)?"
        } else {
            requestString += validateLocationSearchParameters()
        }
        
        requestString += "key=\(NSEClient.sharedInstance.getKey())"
        
        return requestString
    }
    
    fileprivate func validateLocationSearchParameters() -> String {
        if (self.latitude != nil && self.longitude != nil && self.radius != nil) {
            let locationSearchParameters = "lat=\(self.latitude!)&lng=\(self.longitude!)&rad=\(self.radius!)"
            return "?"+locationSearchParameters+"&"
        }
        else if !(self.latitude == nil && self.longitude == nil && self.radius == nil) {
            print("Latitude, longitude, and radius are optionals. But if one is used, all are required.")
            print("You provided lat:\(self.latitude) long:\(self.longitude) radius:\(self.radius)")
            return ""
        }
        
        return "?"
    }

    fileprivate func makeRequest(_ completion:@escaping (_ response:AtmResponse?, _ error: NSError?) -> Void) {
        let requestString = buildRequestUrl()
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.buildRequest(self.requestType!, url: requestString)
        
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = AtmResponse(data: json)
                completion(response, nil)
            }
        })
    }
    
    open func getAtms(_ latitude: Float?, longitude: Float?, radius: String?, completion:@escaping (_ response:AtmResponse?, _ error: NSError?) -> Void) {

        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius

        self.makeRequest(completion)
    }
    
    open func getNextAtms(_ nextPage:String, completion:@escaping (_ response:AtmResponse?, _ error: NSError?) -> Void) {
            
        self.nextPage = nextPage

        self.makeRequest(completion)
    }

    open func getPreviousAtms(_ previousPage:String, completion:@escaping (_ response:AtmResponse?, _ error: NSError?) -> Void) {

        self.previousPage = previousPage
        
        self.makeRequest(completion)
    }

}

open class AtmResponse {
    
    open let previousPage: String
    open let nextPage: String
    open let requestArray: Array<AnyObject>
    
    internal init(data:JSON) {
        self.requestArray = data["data"].arrayValue.map({Atm(data: $0)})
        self.previousPage = data["paging"]["previous"].string ?? ""
        self.nextPage = data["paging"]["next"].string ?? ""
    }
}

open class Atm {
    
    open let atmId: String
    open let name: String
    open let languageList: Array<String>
    open let address: Address
    open let geocode: CLLocation
    open let amountLeft: Int
    open let accessibility: Bool
    open let hours: Array<String>
    
    internal init(data: JSON) {
        self.atmId = data["_id"].string ?? ""
        self.name = data["name"].string ?? ""
        self.languageList = data["language_list"].arrayValue.map {$0.string!}
        self.address = Address(data:data["address"])
        self.amountLeft = data["amount_left"].int ?? 0
        self.accessibility = data["accessibility"].bool ?? false
        self.hours = data["hours"].arrayValue.map {$0.string!}
        self.geocode = CLLocation(latitude: data["lat"].double ?? 0, longitude: data["lng"].double ?? 0)
    }

}
