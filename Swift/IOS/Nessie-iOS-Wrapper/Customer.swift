//
//  Customer.swift
//  Nessie-iOS-Wrapper
//
//  Created by Lopez Vargas, Victor R. on 10/5/15.
//  Copyright (c) 2015 Nessie. All rights reserved.
//

import Foundation
import SwiftyJSON

open class Customer: JsonParser {
    open var firstName: String
    open var lastName: String
    open var address: Address
    open var customerId: String
    
    public init(firstName: String, lastName: String, address: Address, customerId: String) {
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.customerId = customerId
    }
    
    public required init(data: JSON) {
        self.firstName = data["first_name"].string ?? ""
        self.lastName = data["last_name"].string ?? ""
        self.address = Address(data: data["address"])
        self.customerId = data["_id"].string ?? ""
    }
}

open class CustomerRequest {
    fileprivate var requestType: HTTPType!
    fileprivate var accountId: String?
    fileprivate var customerId: String?
    
    public init () {}
    
    fileprivate func buildRequestUrl() -> String {
        
        var requestString = "\(baseString)/customers/"
        if let accountId = accountId {
            requestString = "\(baseString)/accounts/\(accountId)/customer"
        }
        
        if let customerId = customerId {
            requestString += "\(customerId)"
        }

        requestString += "?key=\(NSEClient.sharedInstance.getKey())"
        
        return requestString
    }

    // APIs
    open func getCustomers(_ completion:@escaping (_ customersArrays: Array<Customer>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.GET
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
                let response = BaseResponse<Customer>(data: json)
                completion(response.requestArray, nil)
            }
        })
    }
    
    open func getCustomer(_ customerId: String, completion: @escaping (_ customer: Customer?, _ error: NSError?) -> Void) {
        requestType = HTTPType.GET
        self.customerId = customerId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: requestType)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Customer>(data: json)
                completion(response.object, nil)
            }
        })
    }
    
    open func getCustomerFromAccountId(_ accountId: String, completion: @escaping (_ customersArrays: Customer?, _ error: NSError?) -> Void) {
        requestType = HTTPType.GET
        self.accountId = accountId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: requestType)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Customer>(data: json)
                completion(response.object, nil)
            }
        })
    }
    
    open func postCustomer(_ newCustomer: Customer, completion: @escaping (_ customerResponse: BaseResponse<Customer>?, _ error: NSError?) -> Void) {
        self.requestType = HTTPType.POST
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType)
        
        let address = ["street_number": newCustomer.address.streetNumber,
                       "street_name": newCustomer.address.streetName,
                       "city": newCustomer.address.city,
                       "state": newCustomer.address.state,
                       "zip": newCustomer.address.zipCode]

        let params: Dictionary<String, AnyObject> = ["first_name": newCustomer.firstName as AnyObject,
                                                     "last_name": newCustomer.lastName as AnyObject,
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
                let response = BaseResponse<Customer>(data: json)
                completion(response, nil)
            }
        })
    }
    
    open func putCustomer(_ updatedCustomer: Customer, completion: @escaping (_ customerResponse: BaseResponse<Customer>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.PUT
        customerId = updatedCustomer.customerId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType)
        
        let address = ["street_number": updatedCustomer.address.streetNumber,
                       "street_name": updatedCustomer.address.streetName,
                       "city": updatedCustomer.address.city,
                       "state": updatedCustomer.address.state,
                       "zip": updatedCustomer.address.zipCode]
        
        let params: Dictionary<String, AnyObject> = ["first_name": updatedCustomer.firstName as AnyObject,
                                                     "last_name": updatedCustomer.lastName as AnyObject,
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
                let response = BaseResponse<Customer>(data: json)
                completion(response, nil)
            }
        })
    }
}
