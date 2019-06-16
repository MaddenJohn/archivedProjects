//
//  Purchase.swift
//  Nessie-iOS-Wrapper
//
//  Created by Lopez Vargas, Victor R. on 10/5/15.
//  Copyright (c) 2015 Nessie. All rights reserved.
//

import Foundation
import SwiftyJSON

open class Purchase: JsonParser {
    open var merchantId: String
    open let status: BillStatus
    open var medium: TransactionMedium
    open let payerId: String?
    open var amount: Double
    open let type: String?
    open var purchaseDate: Date?
    open var description: String?
    open let purchaseId: String
    
    public init(merchantId: String, status: BillStatus, medium: TransactionMedium, payerId: String?, amount: Double, type: String, purchaseDate: Date?, description: String?, purchaseId: String) {
        self.merchantId = merchantId
        self.status = status
        self.medium = medium
        self.payerId = payerId
        self.amount = amount
        self.type = type
        self.purchaseDate = purchaseDate
        self.description = description
        self.purchaseId = purchaseId
    }
    
    public required init(data: JSON) {
        self.merchantId = data["merchant_id"].string ?? ""
        self.status = BillStatus(rawValue: data["status"].string ?? "") ?? .Unknown
        self.medium = TransactionMedium(rawValue: data["medium"].string ?? "") ?? .Unknown
        self.payerId = data["payer_id"].string
        self.amount = data["amount"].double ?? 0.0
        self.type = data["type"].string ?? ""
        let transactionDateString = data["purchase_date"].string
        if let str = transactionDateString {
            if let date = dateFormatter.date(from: str) {
                self.purchaseDate = date
            } else {
                self.purchaseDate = Date() as Date
            }
        }
        self.description = data["description"].string
        self.purchaseId = data["_id"].string ?? ""
    }
}

open class PurchaseRequest {
    fileprivate var requestType: HTTPType!
    fileprivate var accountId: String?
    fileprivate var purchaseId: String?
    fileprivate var merchantId: String?
    
    public init () {}
    
    fileprivate func buildRequestUrl() -> String {
        
        var requestString = "\(baseString)/purchases/"
        
        if let merchantId = merchantId, let accountId = accountId {
            requestString = "\(baseString)/merchants/\(merchantId)/accounts/\(accountId)/purchases"
        }
        
        if let merchantId = merchantId {
            requestString = "\(baseString)/merchants/\(merchantId)/purchases"
        }

        if let accountId = accountId {
            requestString = "\(baseString)/accounts/\(accountId)/purchases"
        }
        
        if let purchaseId = purchaseId {
            requestString += "\(purchaseId)"
        }
        
        requestString += "?key=\(NSEClient.sharedInstance.getKey())"
        
        return requestString
    }
    
    // APIs
    open func getPurchase(_ purchaseId: String, completion: @escaping (_ purchase: Purchase?, _ error: NSError?) -> Void) {
        requestType = HTTPType.GET
        self.purchaseId = purchaseId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: requestType)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Purchase>(data: json)
                completion(response.object, nil)
            }
        })
    }
    
    open func getPurchasesFromMerchantId(_ merchantId: String, completion: @escaping (_ purchaseArrays: Array<Purchase>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.GET
        self.merchantId = merchantId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: requestType)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Purchase>(data: json)
                completion(response.requestArray, nil)
            }
        })
    }
    
    open func getPurchasesFromAccountId(_ accountId: String, completion: @escaping (_ purchaseArrays: Array<Purchase>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.GET
        self.accountId = accountId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: requestType)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Purchase>(data: json)
                completion(response.requestArray, nil)
            }
        })
    }
    
    open func getPurchasesFromMerchantAndAccountIds(_ merchantId: String, accountId: String, completion: @escaping (_ purchaseArrays: Array<Purchase>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.GET
        self.merchantId = merchantId
        self.accountId = accountId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: requestType)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Purchase>(data: json)
                completion(response.requestArray, nil)
            }
        })
    }
    
    open func postPurchase(_ newPurchase: Purchase, accountId: String, completion: @escaping (_ purchaseResponse: BaseResponse<Purchase>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.POST
        self.accountId = accountId
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType)
        var params: Dictionary<String, AnyObject> = ["medium": newPurchase.medium.rawValue as AnyObject,
                                                     "merchant_id": newPurchase.merchantId as AnyObject,
                                                     "amount": newPurchase.amount as AnyObject]
        
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-dd-MM"
        if let purchaseDate = newPurchase.purchaseDate as Date? {
            let dateString = dateFormatter.string(from: purchaseDate)
            params["purchase_date"] = dateString as AnyObject?
        }
        
        if let description = newPurchase.description {
            params["description"] = description as AnyObject?
        }
        
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
                let response = BaseResponse<Purchase>(data: json)
                completion(response, nil)
            }
        })
    }
    
    open func putPurchase(_ updatedPurchase: Purchase, completion: @escaping (_ purchaseResponse: BaseResponse<Purchase>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.PUT
        purchaseId = updatedPurchase.purchaseId
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType)
        
        var params: Dictionary<String, AnyObject> = ["medium": updatedPurchase.medium.rawValue as AnyObject,
                                                     "amount": updatedPurchase.amount as AnyObject]
        if let description = updatedPurchase.description {
            params["description"] = description as AnyObject?
        }
        
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
                let response = BaseResponse<Purchase>(data: json)
                completion(response, nil)
            }
        })
    }
    
    open func deletePurchase(_ purchaseId: String, completion: @escaping (_ purchaseResponse: BaseResponse<Purchase>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.DELETE
        self.purchaseId = purchaseId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let response = BaseResponse<Purchase>(requestArray: nil, object: nil, message: "Purchase deleted")
                completion(response, nil)
            }
        })
    }
}
