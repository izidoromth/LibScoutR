import {animate, state, style, transition, trigger} from '@angular/animations';
import { Component, OnInit, ViewChild } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { ApiService } from '../services/api/api.service';
import { Book } from '../models/book';

@Component({
  selector: 'app-misplaced-book',
  templateUrl: './misplaced-book.component.html',
  styleUrls: ['./misplaced-book.component.css'],
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({height: '0px', minHeight: '0'})),
      state('expanded', style({height: '*'})),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ]),
  ],
})
export class MisplacedBookComponent implements OnInit {

  constructor(private apiService: ApiService) { 
  }

  books: Book[] = [];
  displayedColumns: string[] = ['currentCategory', 'id', 'category'];
  expandedElement!: Book | null;
  dataSource = new MatTableDataSource(this.books);

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

}
