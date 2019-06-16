//
//  Merchant.swift
//  Nessie-iOS-Wrapper
//
//  Created by Lopez Vargas, Victor R. (CONT) on 9/1/15.
//  Copyright (c) 2015 Nessie. All rights reserved.
//

import Foundation
import SwiftyJSON

open class Merchant: JsonParser {
    
    open let merchantId: String
    open var name: String
    open var category: Array<String>
    open var address: Address
    open var geocode: Geocode
    
    public init(merchantId: String, name: String, category: Array<String>, address: Address, geocode: Geocode) {
        self.merchantId = merchantId
        self.name = name
        self.category = category
        self.address = address
        self.geocode = geocode
    }
    
    public required init(data: JSON) {
        self.merchantId = data["_id"].string ?? ""
        self.name = data["name"].string ?? ""
        self.category = data["category"].arrayValue.map({$0.string ?? ""})
        self.address = Address(data: data["address"])
        self.geocode = Geocode(data: data["geocode"])
    }
}

open class MerchantRequest {
    fileprivate var requestType: HTTPType!
    fileprivate var merchantId: String?
    fileprivate var rad: String?
    fileprivate var geocode: Geocode?
    
    public init () {}
    
    fileprivate func buildRequestUrl() -> String {
        
        var requestString = "\(baseString)/merchants"
        if let merchantId = merchantId {
            requestString += "/\(merchantId)"
        }
        if let geocode = geocode, let rad = rad {
            requestString += "?lat=\(geocode.lat)&lng=\(geocode.lng)&rad=\(rad)&key=\(NSEClient.sharedInstance.getKey())"
            return requestString
        }
        
        requestString += "?key=\(NSEClient.sharedInstance.getKey())"
        
        return requestString
    }
    
    // APIs
    open func getMerchants(_ geocode: Geocode? = nil, rad: String? = nil, completion:@escaping (_ merchantsArrays: Array<Merchant>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.GET
        self.geocode = geocode
        self.rad = rad
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: requestType)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                guard let data = data else {
                    completion(nil, genericError)
                    return
                }
                let json = JSON(data: data)
                let response = BaseResponse<Merchant>(data: json)
                completion(response.requestArray, nil)
            }
        })
    }
    
    open func getMerchant(_ merchantId: String, completion: @escaping (_ merchant: Merchant?, _ error: NSError?) -> Void) {
        requestType = HTTPType.GET
        self.merchantId = merchantId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: requestType)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Merchant>(data: json)
                completion(response.object, nil)
            }
        })
    }
    
    open func postMerchant(_ newMerchant: Merchant, completion: @escaping (_ merchantResponse: BaseResponse<Merchant>?, _ error: NSError?) -> Void) {
        self.requestType = HTTPType.POST
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType)
        
        let address = ["street_number": newMerchant.address.streetNumber,
                       "street_name": newMerchant.address.streetName,
                       "city": newMerchant.address.city,
                       "state": newMerchant.address.state,
                       "zip": newMerchant.address.zipCode]
        let geocode = ["lng": newMerchant.geocode.lng,
                       "lat": newMerchant.geocode.lat]
        
        let params: Dictionary<String, AnyObject> = ["name": newMerchant.name as AnyObject,
                                                     "category": newMerchant.category as AnyObject,
                                                     "geocode": geocode as AnyObject,
                                                     "address": address as AnyObject]
        
        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: params, options: [])
        } catch let error as NSError {
            request.httpBody = nil
            completion(nil, error)
        }
        
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Merchant>(data: json)
                completion(response, nil)
            }
        })
    }
    
    open func putMerchant(_ updatedMerchant: Merchant, completion: @escaping (_ merchantResponse: BaseResponse<Merchant>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.PUT
        merchantId = updatedMerchant.merchantId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType)
        
        let address = ["street_number": updatedMerchant.address.streetNumber,
                       "street_name": updatedMerchant.address.streetName,
                       "city": updatedMerchant.address.city,
                       "state": updatedMerchant.address.state,
                       "zip": updatedMerchant.address.zipCode]
        let geocode = ["lng": updatedMerchant.geocode.lng,
                       "lat": updatedMerchant.geocode.lat]
        
        let params: Dictionary<String, AnyObject> = ["name": updatedMerchant.name as AnyObject,
                                                     "category": updatedMerchant.category as AnyObject,
                                                     "geocode": geocode as AnyObject,
                                                     "address": address as AnyObject]
        
        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: params, options: [])
        } catch let error as NSError {
            request.httpBody = nil
            completion(nil, error)
        }
        
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Merchant>(data: json)
                completion(response, nil)
            }
        })
    }
}
