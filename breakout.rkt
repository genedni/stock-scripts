#lang racket

(require csv-reading)
(require gregor)

(define breakouts (csv->list (open-input-file "c:/Users/genep/OneDrive/src/data/breakouts-s/breakouts.txt")))

(define csv (csv->list (open-input-file "c:/Users/genep/OneDrive/src/data/breakouts-s/dkng.txt")))

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

;;; Return a hash table of the column names -> position
(define (proc-hdr hdr proc-table)
  (define cols (make-hash))
  (define hdr1 (append hdr (list "tmp")))
  (define count 0)
  (for ([col (in-list hdr)])
    (hash-set! cols col count)
    (set! count (+ count 1)))
  (for ([col (in-list (hash-keys proc-table))])
    (hash-set! cols col count)
    (set! count (+ count 1)))
  cols)

;;; Convert the values in each raw row - string->date and string->number
(define (proc-row row-raw)
  (append (list (~t (parse-datetime (first row-raw) "M/d/y h:m:s a") "yyyyMMdd") (map string->number (rest row-raw)))))

;;; Process the data from the CSV, converting the original lists into vectors for easier processing
(define (proc-data data-raw cols proc-table)
  (define data '())
  (for ([row-raw (in-list data-raw)])
    (define row (proc-row row-raw))
    (set! data (cons row data))
    )
  (set! data (reverse data))
  (set! data (map list->vector data))
  data)

(define (proc-data-hash data-raw cols proc-table)
  (define data (make-hash))
  (for ([row-raw (in-list data-raw)])
    (define row (proc-row row-raw))
    (hash-set! data (first row) (first (map list->vector (rest row))))
    )
  data)

;;; Return a function to maintain a rolling FIFO queue of size <count>
(define (add-and-drop count)
  (let ([l '()])
    (define (add-and-drop value)
      (if (< (length l) count)
          (set! l (append l (list value)))            ;; If the list is shorter than our max size, just add the new value to the list
          (set! l (append (rest l) (list value))))    ;; Otherwise drop the first value and add the new value to the back of the list
      l)
    add-and-drop))

;;; Return a function to calculate the simple moving average of size <window>
(define (sma window)
  (let ([l '()]
        [ad (add-and-drop window)]) ;; Update the sample list, adding the new value and dropping the extra old value if necessary
    (define (sma value)
      (set! l (ad value))
      (if (< (length l) window)     ;; If the list is shorter than our window size, return 0, otherwise return the average of the samples in the list
          0.0
          (/ (apply + l) (length l))))
    sma))

(define (proc-table)
  (define h (make-hash))
;;  (hash-set! h "SMA10" (sma 10))
;;  (hash-set! h "SMA30" (sma 30))
  h)

(define (next-trading-day d holidays [count 1])  ;; TODO - account for holidays, jump multiple days
  (define next-day d)
  (for ([i (in-range 1 (+ count 1))])
    (cond
      [(equal? (~t next-day "e") "6") (set! next-day (+days next-day 3))] ;; Friday > Monday
      [(equal? (~t next-day "e") "7") (set! next-day (+days next-day 2))] ;; Saturday > Monday
      [else (set! next-day (+days next-day 1))])
    (if (hash-has-key? holidays (~t next-day "yyyyMMdd"))
        (set! next-day (next-trading-day next-day holidays))
        next-day))
  next-day)

(define (prev-trading-day d holidays [count 1])  ;; TODO - account for holidays, jump multiple days
  (define prev-day d)
  (for ([i (in-range 1 (+ count 1))])
    (cond
      [(equal? (~t prev-day "e") "1") (set! prev-day (-days prev-day 2))] ;; Sunday > Friday
      [(equal? (~t prev-day "e") "2") (set! prev-day (-days prev-day 3))] ;; Monday > Friday
      [else (set! prev-day (-days prev-day 1))])
    (if (hash-has-key? holidays (~t prev-day "yyyyMMdd"))
        (set! prev-day (prev-trading-day prev-day holidays))
        prev-day))
  prev-day)

(define (proc-holidays)
  (define h (make-hash))
  (call-with-input-file "c:/Users/genep/OneDrive/src/data/breakouts-s/holidays.txt"
    (λ (port)
      (for ([l (in-lines port)])
        (hash-set! h l '()))))
  h)
  
(define (proc-breakouts breakouts)
  (define p (proc-table))
  (define h '())
  (define d '())
  (for ([breakout (in-list breakouts)])
    (define symbol (first breakout))
    (printf "Processing ~a:~n" symbol)
    (define csv (csv->list (open-input-file (format "c:/Users/genep/OneDrive/src/data/breakouts-s/~a.txt" symbol))))
    (set! h (proc-hdr (first csv) p))
    (set! d (proc-data-hash (rest csv) h p))
    (for ([date (in-list (rest breakout))])
      (printf "Looking for ~a on ~a~n" symbol date)
      (define bdata (hash-ref d date))
      (printf "Result: ~a - ~a: Open: ~a High: ~a Low: ~a Close: ~a~n"
              symbol date
              (vector-ref bdata (hash-ref h "Open")) (vector-ref bdata (hash-ref h "Close")) (vector-ref bdata (hash-ref h "Low")) (vector-ref bdata (hash-ref h "Close")))
      )))
