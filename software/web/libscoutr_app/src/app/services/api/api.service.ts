import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Book } from '../../models/book';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseUrl:string = 'http://localhost:5001/';
  private rPiUrl:string = 'http://localhost:5000/';

  constructor(private http: HttpClient) { }

  getBooks(){
    return this.http.get<Book[]>(this.baseUrl+'books')
  };

  correctBook(book: Book){
    let json_book = {
      "current_category": book.category,
      "status": "0",
      "id": book.id
    };

    console.log(json_book);

    return this.http.post(this.baseUrl+'correct_book', json_book);
  };

  searchBook(book: Book){
    let json_book = JSON.stringify({
      "name": book.title, 
      "universal_code": book.id, 
      "current_category": book.current_category
    });

    return this.http.post(this.rPiUrl+'/guide_user', json_book);
  }

}
