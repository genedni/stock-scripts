#lang racket

(require csv-reading)

(define csv (csv->list (open-input-file "test.csv")))

(define hdr-raw (first csv))

(define data-raw (rest csv))

(define (print-row hdr row)
  (cond
    [(empty? row) 0]
    [else
      (printf "~a: ~a " (first hdr) (first row))
      (print-row (rest hdr) (rest row))]))

(define (print-csv hdr data)
  (define hdr-p (proc-hdr hdr))
  (define data-p (proc-data data))
  (for ([row (in-list data-p)])
    (print-row hdr-p row)
    (printf "~n")))

(define (proc-hdr hdr)
  (define hdr1 (append hdr (list "tmp")))
  hdr1)

(define (proc-row row-raw)
  (define row (append (list (first row-raw)) (map string->number (rest row-raw))))
  (set! row (append row (list (/ (apply + (rest row)) (- (length row) 1)))))
  row)

(define (proc-data data-raw)
  (define data '())
  (for ([row-raw (in-list data-raw)])
    (define row (proc-row row-raw))
    (set! data (cons row data))
    )
  (set! data (reverse data))
  (map list->vector data))

(define (add-and-drop count)
  (let ([l '()])
    (define (add-and-drop value)
      (cond [(< (length l) count)]
            [(set! l (append l (list value)))]
            [else
             (set! l (append (rest l) (list value)))])
      l)
    add-and-drop))
