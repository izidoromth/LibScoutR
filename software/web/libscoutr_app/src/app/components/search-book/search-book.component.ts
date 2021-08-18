import {animate, state, style, transition, trigger} from '@angular/animations';
import { Component, OnInit, ViewChild } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { ApiService } from '../../services/api/api.service';
import { Book } from '../../models/book';

@Component({
  selector: 'app-search-book',
  templateUrl: './search-book.component.html',
  styleUrls: ['./search-book.component.css'],
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({height: '0px', minHeight: '0'})),
      state('expanded', style({height: '*'})),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ]),
  ],
})
export class SearchBookComponent implements OnInit {

  constructor(private apiService: ApiService) { 
  }

  books: Book[] = [];
  displayedColumns: string[] = ['title', 'author'];
  expandedElement!: Book;
  dataSource = new MatTableDataSource(this.books);
  clickedRow: Book | null = null;
  searching: Boolean = false;

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  ngOnInit(): void {
    this.apiService.getBooks().subscribe((data: Book[]) => {
      data.forEach(element => {
        this.books.push(element)
      });
      this.dataSource = new MatTableDataSource(this.books);
      this.dataSource.paginator = this.paginator;
    });
  }


  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  searchBook(book: Book) {
    this.searching = true;
    let body = document.getElementById('body');
    let spinner = document.getElementById('spinner');

    this.apiService.searchBook(book).subscribe(res => {
      if(spinner && body){
        body.style.overflow = 'scroll';
        spinner.style.display = 'none';
      }
    })
    if(spinner && body){
      body.style.overflow = 'hidden';
      spinner.style.display = 'block';
    }
  }
}
