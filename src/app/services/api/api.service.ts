import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Book } from '../../models/book';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseUrl:string = 'http://localhost:3000/'

  constructor(private http: HttpClient) { }

  getBooks(){
    return this.http.get<Book[]>(this.baseUrl+'books')
  };

}
