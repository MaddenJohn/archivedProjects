//
//  Bill.swift
//  Nessie-iOS-Wrapper
//
//  Created by Lopez Vargas, Victor R. on 10/5/15.
//  Copyright (c) 2015 Nessie. All rights reserved.
//

import Foundation
import SwiftyJSON

public enum BillStatus : String {
    case Pending = "pending"
    case Recurring = "recurring"
    case Cancelled = "cancelled"
    case Completed = "completed"
    case Unknown
}

open class Bill: JsonParser {
    
    open let billId: String
    open let status: BillStatus
    open var payee: String
    open var nickname: String? = nil
    open var creationDate: Date?
    open var paymentDate: Date? = nil
    open var recurringDate: Int?
    open var upcomingPaymentDate: Date? = nil
    open let paymentAmount: Int
    open var accountId: String
    
    public init (status: BillStatus, payee: String, nickname: String?, creationDate: Date?, paymentDate: Date?, recurringDate: Int?, upcomingPaymentDate: Date?, paymentAmount: Int, accountId: String) {
        self.billId = ""
        self.status = status
        self.payee = payee
        self.nickname = nickname
        self.creationDate = creationDate
        self.paymentDate = paymentDate
        self.recurringDate = recurringDate
        self.upcomingPaymentDate = upcomingPaymentDate
        self.paymentAmount = paymentAmount
        self.accountId = accountId
    }
    
    public required init (data: JSON) {
        self.billId = data["_id"].string ?? ""
        self.status = BillStatus(rawValue: data["status"].string ?? "") ?? .Unknown
        self.payee = data["_payee"].string ?? ""
        self.nickname = data["nickname"].string ?? ""
        
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-dd-MM"

        self.creationDate = dateFormatter.date(from: data["creation_date"].string ?? "")
        self.paymentDate = dateFormatter.date(from: data["payment_date"].string ?? "")
        self.recurringDate = data["recurring_date"].int ?? 0
        self.upcomingPaymentDate = dateFormatter.date(from: data["upcoming_payment_date"].string ?? "")
        self.paymentAmount = data["payment_amount"].int ?? 0
        self.accountId = data["account_id"].string ?? ""
    }
}

open class BillRequest {
    fileprivate var requestType: HTTPType!
    fileprivate var billId: String?
    fileprivate var accountId: String?
    fileprivate var accountType: AccountType?
    fileprivate var customerId: String?

    public init () {}
    
    fileprivate func buildRequestUrl() -> String {

        var requestString = "\(baseString)"
        if (self.accountId != nil) {
            requestString += "/accounts/\(self.accountId!)/bills"
        }

        if (self.billId != nil) {
            requestString += "/bills/\(self.billId!)"
        }
        
        if (self.customerId != nil) {
            requestString = "\(baseString)/customers/\(self.customerId!)/bills"
        }
        
        if (self.requestType == HTTPType.POST) {
            requestString = "\(baseString)/accounts/\(self.accountId!)/bills"
        }
        
        if (self.requestType == HTTPType.GET && self.accountId == nil && self.accountType != nil) {
            var typeParam = self.accountType!.rawValue
            typeParam = typeParam.replacingOccurrences(of: " ", with: "%20")
            requestString += "?type=\(typeParam)&key=\(NSEClient.sharedInstance.getKey())"
            return requestString
        }
        
        requestString += "?key=\(NSEClient.sharedInstance.getKey())"
        
        return requestString
    }
    
    // APIs
    open func getAccountBills(_ accountId: String, completion: @escaping (_ billsArrays: Array<Bill>?, _ error: NSError?) -> Void) {
        self.requestType = HTTPType.GET
        self.accountId = accountId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType!)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Bill>(data: json)
                completion(response.requestArray, nil)
            }
        })
    }
    
    open func getBill(_ billId: String, completion: @escaping (_ bill:Bill?, _ error: NSError?) -> Void) {
        self.requestType = HTTPType.GET
        self.billId = billId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType!)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Bill>(data: json)
                completion(response.object, nil)
            }
        })
    }
    
    open func getCustomerBills(_ customerId: String, completion: @escaping (_ billsArrays: Array<Bill>?, _ error: NSError?) -> Void) {
        self.requestType = HTTPType.GET
        self.customerId = customerId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType!)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Bill>(data: json)
                completion(response.requestArray, nil)
            }
        })
    }
    
    open func postBill(_ newBill: Bill, completion: @escaping (_ billResponse: BaseResponse<Bill>?, _ error: NSError?) -> Void) {
        
        self.requestType = HTTPType.POST
        self.accountId = newBill.accountId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType!)
        
        var params: Dictionary<String, AnyObject> = ["status": newBill.status.rawValue as AnyObject, "payee": newBill.payee as AnyObject, "payment_amount": newBill.paymentAmount as AnyObject]

        if let nickname = newBill.nickname as String? {
            params["nickname"] = nickname as AnyObject?
        }
        
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-dd-MM"
        
        if let paymentDate = newBill.paymentDate as Date? {
            let dateString = dateFormatter.string(from: paymentDate)
            params["payment_date"] = dateString as AnyObject?
        }
        
        if let recurringDate = newBill.recurringDate as Int? {
            params["recurring_date"] = recurringDate as AnyObject?
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
                let response = BaseResponse<Bill>(data: json)
                completion(response, nil)
            }
        })
    }
    
    open func putBill(_ updatedBill: Bill, completion: @escaping (_ billResponse: BaseResponse<Bill>?, _ error: NSError?) -> Void) {
        self.requestType = HTTPType.PUT
        self.billId = updatedBill.billId

        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType!)
        
        var params: Dictionary<String, AnyObject> = ["status": updatedBill.status.rawValue as AnyObject, "payee": updatedBill.payee as AnyObject, "payment_amount": updatedBill.paymentAmount as AnyObject]
        
        if let nickname = updatedBill.nickname as String? {
            params["nickname"] = nickname as AnyObject?
        }
        
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-dd-MM"
        
        if let paymentDate = updatedBill.paymentDate as Date? {
            let dateString = dateFormatter.string(from: paymentDate)
            params["payment_date"] = dateString as AnyObject?
        }
        
        if let recurringDate = updatedBill.recurringDate as Int? {
            params["recurring_date"] = recurringDate as AnyObject?
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
                let response = BaseResponse<Bill>(data: json)
                completion(response, nil)
            }
        })
    }
    
    open func deleteBill(_ billId: String, completion: @escaping (_ billResponse: BaseResponse<Bill>?, _ error: NSError?) -> Void) {
        self.requestType = HTTPType.DELETE
        self.billId = billId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType!)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let response = BaseResponse<Bill>(requestArray: nil, object: nil, message: "Bill deleted")
                completion(response, nil)
            }
        })
    }
}
