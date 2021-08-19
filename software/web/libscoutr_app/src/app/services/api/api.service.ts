import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Book } from '../../models/book';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseUrl:string = 'http://10.0.0.169:5001/';
  private rPiUrl:string = 'http://localhost:5000/';

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

    return this.http.post(this.rPiUrl+'/guide_user', json_book);
  }

}
