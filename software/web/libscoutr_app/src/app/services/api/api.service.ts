import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Book } from '../../models/book';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseUrl:string = 'http://localhost:5001/'

  constructor(private http: HttpClient) { }

  getBooks(){
    return this.http.get<Book[]>(this.baseUrl+'books')
  };

  searchBook(book: Book){
    let json_book = JSON.stringify({
      "name": book.title, 
      "universal_code": book.id, 
      "current_category": book.current_category
    });

    return this.http.post(this.baseUrl+'/guide_user', json_book);
  }

}
